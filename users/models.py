import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unit_system = models.CharField(max_length=10, default="metric")
    timezone = models.CharField(max_length=50, default="UTC")
    theme = models.CharField(max_length=20, default="light")


class Invitation(models.Model):
    email = models.EmailField(unique=True) 
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    inviter_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4()
        if self.invited_by and not self.inviter_email:
            self.inviter_email = self.invited_by.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invite to {self.email} from {self.invited_by.email}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile whenever a new User is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
