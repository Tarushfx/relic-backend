from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # 1. Your Custom API Logic (Profile, Invite, etc.)
    path("api/users/", include("users.urls")),
    # 2. JWT Logic (The actual login for your API)
    # TODO: customise this
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 3. Django Default Auth (Useful ONLY for Password Reset emails)
    path("api/auth/", include("django.contrib.auth.urls")),
]
