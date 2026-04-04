from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/core/", include("core.urls")),
    # path("api/users/", include("users.urls")),
    path("api/auth/", include("django.contrib.auth.urls")),
]
