import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unit_system = models.CharField(max_length=10, default="metric")
    timezone = models.CharField(max_length=50, default="UTC")
    theme = models.CharField(max_length=20, default="light")


class Invitation(models.Model):
    email = models.EmailField()

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite to {self.email} from {self.invited_by.email}"
