from email.policy import default
from enum import auto
from django.utils import timezone

from rest_framework import serializers

from logs.models import LogDefinition, LogEntry
from ..constants import type_mapping


class LogTableRequestSerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)


class LogDefinitionRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    fields = serializers.JSONField()

    class Meta:
        model = LogDefinition
        fields = ["name", "description", "fields"]

    def validate_fields(self, fields):
        if not fields or not isinstance(fields, dict):
            raise serializers.ValidationError("Fields must be a non-empty dictionary.")


class LogEntryRequestSerializer(serializers.ModelSerializer):
    values = serializers.JSONField()
    timestamp = serializers.DateTimeField(
        required=False,  # Make False if you want to use the default
        format="%Y-%m-%d %H:%M:%S",
        default=timezone.now,
    )
    source = serializers.CharField(required=False, default="user")

    class Meta:
        model = LogEntry
        fields = ["values", "timestamp", "source"]

    def validate_values(self, values):
        # 1. Basic structure check
        if not isinstance(values, dict):
            raise serializers.ValidationError("Values must be a dictionary.")

        log_definition = self.context.get("log_definition")
        if not log_definition:
            return values

        fields_config = log_definition.fields  # Your table definition
        final_values = {}
        errors = {}

        for field_name, config in fields_config.items():
            val = values.get(field_name)

            if val is None:
                errors[field_name] = (
                    "This field is required based on the table definition."
                )
                continue

            expected_str = config.get("datatype")
            expected_type = type_mapping.get(expected_str)

            if not expected_type or not isinstance(val, expected_type):
                errors[field_name] = (
                    f"Expected {expected_str}, got {type(val).__name__}."
                )
            else:
                final_values[field_name] = val

        if errors:
            raise serializers.ValidationError(errors)

        return final_values
