from rest_framework import (
    serializers
)
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .authentication import (
    decode_access_token,
    create_access_token,
    decode_refresh_token
)

class UserSerializer(serializers.ModelSerializer):
    """serializer for creating user"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """create new user"""
        return get_user_model().objects.create_user(**validated_data)
