from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import User

from .models import Post


fields = ('user', 'title', 'description', 'body')


class PostSerializer(serializers.ModelSerializer):
   class Meta:
        model = Post
        fields = fields

    