from rest_framework import generics
from rest_framework.response import Response
# from rest_framework import exceptions
from .serializers import (
    UserSerializer,
)
from django.contrib.auth import get_user_model
from .authentication import create_access_token

class RegisterGenericView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, serializer):
        data = serializer.data

        if data['password'] != data['password_confirm']:
            raise ValueError('Password do not match!')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginGenericView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, serializer):
        data = serializer.data

        email = data['email']
        password = data['password']

        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        user = get_user_model().objects.filter(email=email).first()

        if user is None:
            raise ValueError("Invalid Credential")

        if not user.check_password(password):
            raise ValueError("Invalid Credential")

        access_token = create_access_token(user.id)
        refresh_token = create_access_token(user.id)

        response = Response()

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True
        )

        response.data = {
            'token': access_token,
        }

        return response