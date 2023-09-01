from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model


from .models import Profile
User = get_user_model()
# Readers = apps.get_model('read_stats', 'Readers')


class ProfileListSerializer(serializers.ModelSerializer):
    """List the profiles."""

    class Meta:
        """Define the serializer META data."""

        model = Profile
        fields = ('user')
