from django.db import models

from config import settings


class LogDefinition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fields = models.JSONField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    meta = models.JSONField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=models.Q(is_deleted=False),
                name="unique_active_name",
            )
        ]

    def __str__(self):
        return self.name


class LogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    log_definition = models.ForeignKey(
        LogDefinition, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now=True)
    values = models.JSONField()
    source = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"LogEntry {self.id} for {self.log_definition.name if self.log_definition else 'No Definition'}"
