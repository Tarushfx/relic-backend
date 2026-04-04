from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InviteUserView, ProfileViewSet, UserSignupView

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("invite/", InviteUserView.as_view(), name="invite-user"),
    path("signup/", UserSignupView.as_view(), name="signup"),
]
