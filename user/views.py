from rest_framework import (
    generics,
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework.response import Response
# from rest_framework import exceptions
from user import serializers

from .authentication import (
    create_access_token,
    create_refresh_token,
    JWTAuthentication,
    decode_refresh_token
)
from core.models import (
    User,
    UserToken,
    Reset,
)
import datetime, random, string
from config.mail import send_email

class RegisterGenericView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

    def create(self, serializer):
        data = serializer.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password do not match!')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginGenericView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def create(self, serializer):
        data = serializer.data
        queryset = self.queryset

        email = data['email']
        password = data['password']

        if not email:
            raise exceptions.APIException("Email is required")

        if not password:
            raise exceptions.APIException("Password is required")

        user = queryset.filter(email=email).first()

        if user is None:
            raise exceptions.APIException("Invalid Credential")

        if not user.check_password(password):
            raise exceptions.APIException("Invalid Credential")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            user = user.id,
            token = refresh_token,
            expired_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )

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
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RefreshGenericView(generics.CreateAPIView):
    serializer_class = serializers.RefreshTokenSerializer
    queryset = UserToken.objects.all()

    def create(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not self.queryset.filter(
            user = id,
            token = refresh_token,
            expired_at__gt = datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed("Unauthenticated")

        access_token = create_access_token(id)

        response = Response()

        response.data = {
            'token': access_token
        }

        return response

class LogoutGenericView(generics.CreateAPIView):
    def create(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        UserToken.objects.filter(token=refresh_token).delete()

        response = Response()

        response.delete_cookie(key='refresh_token')

        response.data = {
            'message': 'logout successfully!'
        }

        return response

class ForgotGenericView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.ForgotSerializer
    queryset = Reset.objects.all()

    def perform_create(self, serializer):
        email = self.request.data['email']
        email_exists = self.queryset.filter(email=email).first()

        if email_exists is not None:
            email_exists.delete()

        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        url = 'http://localhost:3000/forgot-password/' + token

        res = send_email(url, email)

        if res != 1:
            raise exceptions.APIException('Email not send')
        serializer.save(email=email, token=token)

class ResetPasswordGenericView(generics.UpdateAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    queryset = User.objects.all()

    def update(self, serializer):
        data = serializer.data

        pk = serializer.GET.get('id')

        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise exceptions.APIException('Password not match!')

        reset_password = Reset.objects.filter(token=pk).first()

        if not reset_password:
            raise exceptions.APIException('Invalid Link!')

        user = self.queryset.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('User not found!')

        user.set_password(password)
        user.save()
        reset_password.delete()

        return Response({
            'message': 'Password Changed Successfully!'
        })