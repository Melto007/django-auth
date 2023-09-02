"""
Django models for creating tables
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)

class UserManager(BaseUserManager):
    """create user"""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email field is required")

        if not password:
            raise ValueError("Password field is required")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """User models table for creating users"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = []
