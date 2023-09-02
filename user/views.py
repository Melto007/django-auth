from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
# from rest_framework import exceptions
from .serializers import (
    UserSerializer,
)
from django.contrib.auth import get_user_model
from .authentication import (
    create_access_token,
    create_refresh_token,
    JWTAuthentication,
    decode_refresh_token
)
from rest_framework.authentication import get_authorization_header
from core.models import (
    User
)

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
    queryset = User.objects.all()

    def create(self, serializer):
        data = serializer.data
        queryset = self.queryset

        email = data['email']
        password = data['password']

        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        user = queryset.filter(email=email).first()

        if user is None:
            raise ValueError("Invalid Credential")

        if not user.check_password(password):
            raise ValueError("Invalid Credential")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

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

class UserGenericView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RefreshGenericView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def create(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        access_token = create_access_token(id)

        response = Response()

        response.data = {
            'token': access_token
        }

        return response

class LogoutGenericView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def create(self, request):
        response = Response()

        response.delete_cookie(key='refresh_token')

        response.data = {
            'message': 'logout successfully!'
        }

        return response