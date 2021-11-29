from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from newsfeed.tasks import populate_user_newsfeed

from user.models import UserSettings
from apiconsumer.models import SourceModel
from user.tasks import send_reset_password_mail

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, bad_request

from user.tasks import token_decode
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    UserSerializer,
    RegisterSerializer,
    UserSettingsModelSerializer,
)


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Registers/ create a new user
        """
        serializer: RegisterSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = serializer.save()

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )

    def patch(self, request):
        """
        Pre check/validate if registration can happen or not
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Signs in the user and returns auth token if credentials are okay
        """
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data["user"]

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": str(token)})

    def delete(self, request):
        """
        Logout user by invalidating the token assigned to request.user
        """
        try:
            request.user.auth_token.delete()
        except Exception:
            pass

        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserSettingsAPI(generics.GenericAPIView):
    serializer_class = UserSettingsModelSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        settings, created = UserSettings.objects.get_or_create(user=user)
        serializer = self.get_serializer(instance=settings)
        return Response(serializer.data)

    def post(self, request):
        sources = request.data.get("sources")
        countries = request.data.get("countries")
        keywords = request.data.get("keywords")

        settings, _ = UserSettings.objects.get_or_create(user=request.user)

        if countries:
            settings.countries = ",".join(countries)

        if keywords:
            settings.keywords = keywords

        settings.sources.set(SourceModel.objects.filter(id__in=sources), clear=True)
        settings.save()

        # Invoke async task for updating newsfeed
        populate_user_newsfeed.delay(request.user.id)

        return Response(
            self.get_serializer(instance=settings).data, status=status.HTTP_200_OK
        )


class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            user_id = token_decode(token)
        except Exception as e:
            return bad_request(request, e)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=user_id)
        user.set_password(serializer.validated_data.get("password"))

        return Response(request.data, status=status.HTTP_200_OK)


class InitiateChangePassword(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.GET.get("email")
        callback_url = request.GET.get('callback')

        if not callback_url:
            raise ValidationError({"callback": "callback parameter is required"})

        if not email:
            raise ValidationError({"email": "email parameter is required"})

        if not User.objects.filter(email=email).exists():
            raise ValidationError({"message": "email is not recognized"})

        send_reset_password_mail.delay(request.user.id, request.user.email, callback_url)
        return Response({"message": f"password reset mail was sent to {email}."})


class Profile(generics.GenericAPIView):
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"username": user.username, "email": user.email})
