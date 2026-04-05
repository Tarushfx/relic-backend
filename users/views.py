from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction

from core.views import BaseAPIView
from core.responses import ApiResponse
from .models import Invitation, UserProfile
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

            return self.created_response(
                data={"user_id": user.id, "email": user.email},
                message="User created successfully",
            )
        return self.validation_error_response(serializer.errors)
