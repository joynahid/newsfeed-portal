from django.contrib.auth import authenticate
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
import pycountry
from apiconsumer.api.serializers import SourceModelSerializer
from apiconsumer.const import *
from apiconsumer.models import SourceModel
from user.models import UserSettings
from apiconsumer import const as c


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("password",)

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated):
        user = User.objects.create_user(
            validated["username"],
            validated["email"],
            validated["password"],
        )

        return user

    def validate(self, data):
        data = super().validate(data)

        username = data.get("username")
        password = data.get("password")

        if len(username) < 3:
            raise serializers.ValidationError(
                {"username": "username should be minimum 3 letters"}
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "password should be minimum 8 characters"}
            )

        if "email" not in data:
            raise serializers.ValidationError({"email": "email is required"})

        try:
            validate_email(data.get("email"))
        except DjangoValidationError as e:
            raise serializers.ValidationError({"email": "invalid email address"})

        return data


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        if "username" not in data:
            msg = "username is required"
            raise ValidationError({"username": msg})

        if "password" not in data:
            msg = "password is required"
            raise ValidationError({"password": msg})

        user: User = authenticate(username=data["username"], password=data["password"])

        if not user:
            raise ValidationError({"message": "incorrect username or password"})

        if not user.is_active:
            msg = f"user {user.username} is deactivated"
            raise ValidationError({"message": msg})

        data["user"] = user

        return data


class UserSettingsModelSerializer(serializers.ModelSerializer):
    sources = SourceModelSerializer(many=True, read_only=True)
    countries = serializers.SerializerMethodField()

    class Meta:
        model = UserSettings
        fields = ("sources", "countries", "keywords")

    def get_countries(self, instance):
        return instance.countries.split(',')