from rest_framework import serializers


class LogTableRequestSerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)


class LogDefinitionRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    fields = serializers.JSONField()
