from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Invitation, UserProfile

User = get_user_model()


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class ProfileRequestSerializer(serializers.ModelSerializer):
    user = UserRequestSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "unit_system", "timezone", "theme"]


class InvitationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["email"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        if Invitation.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An invitation has already been sent to this email."
            )
        return value

    def create(self, validated_data):
        validated_data["invited_by"] = self.context["request"].user
        return super().create(validated_data)


class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "A user with this email already exists."}
            )

        if not Invitation.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"token": "Invalid or expired invitation token."}
            )
        return data

    def save(self):
        user = User.objects.create_user(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            password=self.validated_data["password"],
        )
        return user
