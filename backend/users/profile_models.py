from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import User


class UserProfile(models.Model):
    """
    Extended user profile model.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_("user")
    )
    
    # Privacy settings
    PRIVACY_CHOICES = [
        ('public', _('Public')),
        ('friends', _('Friends Only')),
        ('private', _('Private')),
    ]
    
    privacy_setting = models.CharField(
        _("privacy setting"),
        max_length=10,
        choices=PRIVACY_CHOICES,
        default='public',
        help_text=_("Who can see your profile and activity")
    )
    
    # Notification preferences
    email_notifications = models.BooleanField(
        _("email notifications"),
        default=True,
        help_text=_("Receive email notifications for activity")
    )
    
    push_notifications = models.BooleanField(
        _("push notifications"),
        default=True,
        help_text=_("Receive push notifications for activity")
    )
    
    # Social connections
    website = models.URLField(_("website"), blank=True, null=True)
    github_username = models.CharField(_("GitHub username"), max_length=100, blank=True, null=True)
    twitter_username = models.CharField(_("Twitter username"), max_length=100, blank=True, null=True)
    linkedin_username = models.CharField(_("LinkedIn username"), max_length=100, blank=True, null=True)
    
    # Location information
    location = models.CharField(_("location"), max_length=255, blank=True, null=True)
    
    # Professional information
    occupation = models.CharField(_("occupation"), max_length=100, blank=True, null=True)
    company = models.CharField(_("company"), max_length=100, blank=True, null=True)
    
    # Account preferences
    theme_preference = models.CharField(
        _("theme preference"),
        max_length=10,
        choices=[
            ('light', _('Light')),
            ('dark', _('Dark')),
            ('system', _('System Default')),
        ],
        default='system'
    )
    
    language_preference = models.CharField(
        _("language preference"),
        max_length=10,
        choices=[
            ('en', _('English')),
            ('es', _('Spanish')),
            ('fr', _('French')),
            ('de', _('German')),
        ],
        default='en'
    )
    
    # Activity tracking
    last_active = models.DateTimeField(_("last active"), auto_now=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    
    # Profile customization
    profile_background = models.ImageField(
        _("profile background"),
        upload_to="profile_backgrounds/",
        blank=True,
        null=True
    )
    
    # Relationships
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        blank=True,
        symmetrical=False,
        verbose_name=_("following")
    )
    
    blocked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='blocked_by',
        blank=True,
        symmetrical=False,
        verbose_name=_("blocked users")
    )
    
    def __str__(self):
        return f"Profile for {self.user.email}"
    
    def get_followers_count(self):
        """Return the number of followers."""
        return self.user.followers.count()
    
    def get_following_count(self):
        """Return the number of users this profile is following."""
        return self.following.count()
    
    def is_following(self, user):
        """Check if this profile is following the given user."""
        return self.following.filter(id=user.id).exists()
    
    def is_blocking(self, user):
        """Check if this profile is blocking the given user."""
        return self.blocked_users.filter(id=user.id).exists()
    
    def toggle_follow(self, user):
        """Toggle follow status for the given user."""
        if self.is_following(user):
            self.following.remove(user)
            return False
        else:
            self.following.add(user)
            return True
    
    def toggle_block(self, user):
        """Toggle block status for the given user."""
        if self.is_blocking(user):
            self.blocked_users.remove(user)
            return False
        else:
            self.blocked_users.add(user)
            return True
    
    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
        ordering = ['-date_created']