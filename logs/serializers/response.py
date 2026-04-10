from rest_framework import serializers

from logs.models import LogDefinition, LogEntry
from logs.serializers.serializers import LogTableSerializer


class LogTableResponseSerializer(serializers.Serializer):
    # Using a simple Serializer because this is a combined "Shape", not a single Model
    id = serializers.IntegerField(read_only=True)
    table_meta = serializers.DictField()
    rows = LogTableSerializer(many=True)

    class Meta:
        # Serializers.Serializer doesn't strictly need a Meta class,
        # but we can leave it or remove it.
        pass


class LogDefinitionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    fields = serializers.JSONField()

    class Meta:
        pass


class LogEntryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ["id", "values", "created_at", "source", "timestamp"]


class ActivityResponseSerializer(serializers.ModelSerializer):
    # This 'log_definition' must match the field name on your LogEntry model
    log_definition = LogDefinitionResponseSerializer(read_only=True)

    class Meta:
        model = LogEntry
        # List all fields from LogEntry + the nested log_definition
        fields = ["id", "log_definition", "values", "created_at"]
