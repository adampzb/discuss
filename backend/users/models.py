from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    This allows us to add custom fields and methods to the user model.
    """
    
    # Remove username field and use email as the primary identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Add any custom fields here
    bio = models.TextField(_('biography'), blank=True, null=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    
    # Use email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
