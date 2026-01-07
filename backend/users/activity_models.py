from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UserActivity(models.Model):
    """
    Track user activities across the platform.
    """
    
    # Activity types
    ACTIVITY_TYPES = [
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('register', _('Registration')),
        ('profile_update', _('Profile Update')),
        ('password_change', _('Password Change')),
        ('post_create', _('Post Created')),
        ('post_like', _('Post Liked')),
        ('comment_create', _('Comment Created')),
        ('comment_like', _('Comment Liked')),
        ('follow', _('Followed User')),
        ('unfollow', _('Unfollowed User')),
        ('block', _('Blocked User')),
        ('unblock', _('Unblocked User')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name=_("user")
    )
    
    activity_type = models.CharField(
        _("activity type"),
        max_length=50,
        choices=ACTIVITY_TYPES
    )
    
    # Generic relation to any content
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional context
    metadata = models.JSONField(_("metadata"), default=dict, blank=True)
    
    # Location and device info
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("user activity")
        verbose_name_plural = _("user activities")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.get_activity_type_display()} at {self.created_at}"
    
    def get_context_data(self):
        """Get additional context for the activity."""
        context = {
            'type': self.activity_type,
            'user': self.user.email,
            'timestamp': self.created_at,
            'metadata': self.metadata,
        }
        
        if self.content_object:
            context['content_object'] = str(self.content_object)
            context['content_type'] = self.content_type.model
        
        return context


class UserActivityAggregation(models.Model):
    """
    Aggregated user activity statistics for performance.
    """
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_stats',
        verbose_name=_("user")
    )
    
    # Activity counts
    total_activities = models.PositiveIntegerField(_("total activities"), default=0)
    logins = models.PositiveIntegerField(_("logins"), default=0)
    posts_created = models.PositiveIntegerField(_("posts created"), default=0)
    comments_created = models.PositiveIntegerField(_("comments created"), default=0)
    likes_received = models.PositiveIntegerField(_("likes received"), default=0)
    followers_gained = models.PositiveIntegerField(_("followers gained"), default=0)
    
    # Streaks and engagement
    current_streak = models.PositiveIntegerField(_("current streak"), default=0)
    longest_streak = models.PositiveIntegerField(_("longest streak"), default=0)
    last_active = models.DateTimeField(_("last active"), auto_now=True)
    
    # Privacy and visibility
    show_activity = models.BooleanField(_("show activity"), default=True)
    
    class Meta:
        verbose_name = _("user activity aggregation")
        verbose_name_plural = _("user activity aggregations")
    
    def __str__(self):
        return f"Activity stats for {self.user.email}"
    
    def update_from_activity(self, activity):
        """Update aggregation from a new activity."""
        self.total_activities += 1
        
        if activity.activity_type == 'login':
            self.logins += 1
        elif activity.activity_type == 'post_create':
            self.posts_created += 1
        elif activity.activity_type == 'comment_create':
            self.comments_created += 1
        elif activity.activity_type == 'follow':
            self.followers_gained += 1
        
        self.save()


class UserSession(models.Model):
    """
    Track user sessions for security and analytics.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_("user")
    )
    
    session_key = models.CharField(_("session key"), max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    
    # Location data
    country = models.CharField(_("country"), max_length=100, blank=True)
    city = models.CharField(_("city"), max_length=100, blank=True)
    
    # Session info
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    last_activity = models.DateTimeField(_("last activity"), auto_now=True)
    
    class Meta:
        verbose_name = _("user session")
        verbose_name_plural = _("user sessions")
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', '-last_activity']),
            models.Index(fields=['is_active', '-last_activity']),
        ]
    
    def __str__(self):
        return f"Session {self.session_key[:8]}... for {self.user.email}"
    
    def end_session(self):
        """Mark session as ended."""
        self.is_active = False
        self.save()