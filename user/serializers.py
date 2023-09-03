from rest_framework import (
    serializers
)
from django.contrib.auth import get_user_model

from core import models
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    """serializer for creating user"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """create new user"""
        return get_user_model().objects.create_user(**validated_data)

class ResetPasswordSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserSerializer.Meta.model
        fields = ['password']
        extra_kwargs = UserSerializer.Meta.extra_kwargs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, **validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserToken
        fields = ['user', 'token', 'expired_at']

class RefreshTokenSerializer(UserTokenSerializer):
    class Meta(UserTokenSerializer.Meta):
        model = UserTokenSerializer.Meta.model
        fields = UserTokenSerializer.Meta.fields

class ForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reset
        fields = ['email']
        extra_kwargs = {'email': {'write_only': True}}

    def create(self, validated_data):
        return models.Reset.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['message'] = 'Reset token created successfully.'
        return data