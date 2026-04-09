from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from core.views import BaseAPIView
from core.responses import ApiResponse
from users.serializers.responses import UserResponseSerializer
from .models import Invitation, UserProfile, User
from .serializers import (
    ProfileResponseSerializer,
    InvitationRequestSerializer,
    InvitationResponseSerializer,
    SignupRequestSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class InviteUserView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvitationRequestSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            invitation = serializer.save()
            response_data = InvitationResponseSerializer(invitation).data
            return self.created_response(
                data=response_data, message="Invitation sent successfully"
            )
        return self.validation_error_response(serializer.errors)


class UserSignupView(BaseAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupRequestSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                invitation_deleted, _ = Invitation.objects.filter(
                    email=user.email, token=request.data.get("token")
                ).delete()

            refresh = RefreshToken.for_user(user)
            data = {
                "email": user.email,
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            response_data = SignupRequestSerializer(user).data
            return self.created_response(
                data=response_data,
                message="User created successfully",
            )
        return self.validation_error_response(serializer.errors)


class UserDeleteView(BaseAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return self.success_response(message="User deleted successfully")
        except User.DoesNotExist:
            return self.not_found_response(message="User not found")
