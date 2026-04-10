from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from logs.models import LogDefinition, LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry  # Replace with your actual model name
        fields = "__all__"
        read_only_fields = [
            "user",
            "log_definition",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]


class LogDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogDefinition
        fields = "__all__"
        # user is handled by the view, is_deleted and deleted_at are handled by logic
        read_only_fields = ["user", "is_deleted", "deleted_at"]

    def validate_fields(self, fields):
        if not fields or not isinstance(fields, dict):
            raise serializers.ValidationError("Fields must be a non-empty dictionary.")

        # 2. Define required keys for each field definition
        required_keys = ["datatype"]
        allowed_keys = ["datatype", "unit", "visible_unit", "description", "meta"]
        valid_datatypes = ["int", "float", "string", "boolean", "json"]
        final_dict = {}
        for column, values in fields.items():
            current_config = {}
            if not isinstance(values, dict):
                raise serializers.ValidationError(
                    f"Configuration for '{field_name}' must be an object."
                )
            missing_keys = [key for key in required_keys if key not in values]
            if missing_keys:
                raise serializers.ValidationError(
                    f"Missing keys: {', '.join(missing_keys)} for {column}"
                )
            for field_name, value in values.items():
                if field_name not in allowed_keys:
                    continue
                if field_name == "datatype" and value not in valid_datatypes:
                    raise serializers.ValidationError(
                        f"Invalid datatype '{value}' in '{field_name}'. "
                        f"Must be one of: {', '.join(valid_datatypes)}"
                    )
                current_config[field_name] = value
            final_dict[column] = current_config
        return final_dict


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
