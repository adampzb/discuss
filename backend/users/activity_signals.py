from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from .activity_models import UserActivity, UserActivityAggregation, UserSession
from .profile_models import UserProfile


@receiver(post_save, sender="users.User")
def create_user_activity_stats(sender, instance, created, **kwargs):
    """
    Create activity aggregation when a new user is created.
    """
    if created:
        UserActivityAggregation.objects.create(user=instance)

        # Log registration activity
        UserActivity.objects.create(
            user=instance,
            activity_type="register",
            metadata={"method": "email_password"},
        )


@receiver(post_save, sender=UserProfile)
def log_profile_update(sender, instance, **kwargs):
    """
    Log activity when user profile is updated.
    """
    if not kwargs.get("raw", False):
        UserActivity.objects.create(
            user=instance.user,
            activity_type="profile_update",
            metadata={
                "fields_changed": "profile_update"
            },  # Could track specific fields
        )


def log_user_login(sender, request, user, **kwargs):
    """
    Log user login activity.
    """
    # Get client IP and user agent
    ip_address = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # Create activity log
    UserActivity.objects.create(
        user=user,
        activity_type="login",
        ip_address=ip_address,
        user_agent=user_agent,
        metadata={
            "browser": "unknown",  # Could parse user agent
            "os": "unknown",
            "device": "unknown",
        },
    )

    # Update activity aggregation
    try:
        stats = user.activity_stats
        stats.update_from_activity(UserActivity(activity_type="login"))
    except UserActivityAggregation.DoesNotExist:
        pass


def log_user_logout(sender, request, user, **kwargs):
    """
    Log user logout activity.
    """
    UserActivity.objects.create(
        user=user,
        activity_type="logout",
        metadata={"session_duration": "calculated"},  # Could calculate session duration
    )


def create_user_session(sender, request, user, **kwargs):
    """
    Create user session record on login.
    """
    session_key = request.session.session_key
    ip_address = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # Create or update session
    UserSession.objects.update_or_create(
        session_key=session_key,
        defaults={
            "user": user,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "is_active": True,
            "last_activity": timezone.now(),
        },
    )


def end_user_session(sender, request, **kwargs):
    """
    End user session on logout.
    """
    session_key = request.session.session_key

    try:
        session = UserSession.objects.get(session_key=session_key)
        session.end_session()
    except UserSession.DoesNotExist:
        pass


@receiver(pre_delete, sender=Session)
def cleanup_user_session(sender, instance, **kwargs):
    """
    Clean up user session when Django session is deleted.
    """
    try:
        user_session = UserSession.objects.get(session_key=instance.session_key)
        user_session.end_session()
    except UserSession.DoesNotExist:
        pass
