from rest_framework import status, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Invitation, UserProfile
from .serializers import InvitationSerializer, ProfileSerializer, SignupSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    # TODO: read more on this
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users should only be able to see/edit THEIR OWN profile
        return UserProfile.objects.filter(user=self.request.user)


class InviteUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the invite and link it to the person sending it
            serializer.save(invited_by=request.user)
            # In a real app, you'd trigger an email here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignupView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # After successful signup, delete the invitation
            Invitation.objects.filter(email=user.email).delete()
            return Response(
                {"message": "User created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
