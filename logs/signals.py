from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LogDefinition, LogEntry


@receiver(post_save, sender=LogDefinition)
def archive_log_entries(sender, instance, created, **kwargs):
    if not created and instance.is_deleted:
        LogEntry.objects.filter(log_definition=instance).update(is_deleted=True)
