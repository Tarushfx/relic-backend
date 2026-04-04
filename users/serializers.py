from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Invitation, UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    # Nested user data (Read-only)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "unit_system", "timezone", "theme"]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["email", "created_at"]
        read_only_fields = ["created_at"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate_email(self, value):
        # 1. Check if user already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")

        # 2. Check if invitation exists
        if not Invitation.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email has not been invited.")

        return value

    def create(self, validated_data):
        # Create the user using the model manager
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user
