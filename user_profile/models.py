"""Define the user__profile model."""

from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()


class ProfileManager(models.Manager):
    """Define profile model properies."""

    def create_profile(self, **kwargs):
        """Create a profile."""
        self.model.create(user=kwargs['instance'])


class Profile(models.Model):
    """The profile model columns."""

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        _('Profile field', 'created at'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Profile field', 'updated at'),
        auto_now=True
    )


    class Meta:
        """Define the seerializer metadata."""

        app_label = 'user_profile'

    def __str__(self):
        """Define the data print representation."""
        return self.user.username



def create_profile(sender, **kwargs):
    """Create a profile."""
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


create_profile_signal = post_save.connect(create_profile, sender=get_user_model())
