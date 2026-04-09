from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from logs.models import LogDefinition, LogEntry


class TableResultSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry  # Replace with your actual model name
        fields = "__all__"


class LogDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogDefinition  # Replace with your actual model name
        fields = "__all__"


class LogTableSerializer(serializers.ModelSerializer):
    # This nests the full definition object inside the entry
    log_definition = LogDefinitionSerializer(read_only=True)

    # Use this to allow passing just the ID when creating/updating
    log_definition_id = serializers.PrimaryKeyRelatedField(
        queryset=LogDefinition.objects.all(), source="log_definition", write_only=True
    )

    class Meta:
        model = LogEntry
        fields = [
            "id",
            "created_at",
            "log_definition",
            "log_definition_id",
            "values",
            "source",
            "meta",
        ]
