from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Invitation, UserProfile

User = get_user_model()


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class ProfileResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "unit_system", "timezone", "theme"]


class InvitationResponseSerializer(serializers.ModelSerializer):
    inviter_email = serializers.EmailField(source="invited_by.email", read_only=True)

    class Meta:
        model = Invitation
        fields = ["email", "token", "created_at", "inviter_email"]
        read_only_fields = ["token", "created_at"]
