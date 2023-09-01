"""Define the posts model."""

from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from ..user_profile.models import Profile


class Post(models.Model):
    """The post model."""

    user = models.ForeignKey(
        get_user_model(),
        related_name='author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    title = models.CharField(
        _('Post field', 'title'),
        max_length=128
    )
    description = models.TextField(
        _('Post Field', 'description'),
        blank=True,
        null=True
    )
    body = models.TextField(
        _('Article Field', 'body'),
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        _('Post field', 'created at'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Post field', 'updated at'),
        auto_now=True
    )

    liked_by = models.ManyToManyField(
        Profile, related_name='liked_posts', symmetrical=True)
    disliked_by = models.ManyToManyField(
        Profile, related_name='disliked_posts', symmetrical=True)


    def like_post(self, profile):
        """Like a post."""
        profile.liked_posts.add(self)

    def dislike_article(self, profile):
        """Dislike an article."""
        profile.disliked_posts.add(self)

    def unlike_post(self, profile):
        """Unlike a post."""
        profile.liked_posts.remove(self)

    def undislike_post(self, profile):
        """Undislike a post."""
        profile.disliked_posts.remove(self)

    class Meta:
        """define metadata."""

        app_label = 'post'

    def __str__(self):
        """Print out as title."""
        return self.title
