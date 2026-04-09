from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.views import BaseAPIView
from logs.serializers.response import LogDefinitionRequestSerializer
from .models import LogDefinition, LogEntry
from .serializers.serializers import (
    LogDefinitionSerializer,
    LogEntrySerializer,
    LogTableResponseSerializer,
    LogTableSerializer,
    TableResultSetPagination,
)


class LogTableView(BaseAPIView):
    def get(self, request, id):
        log_definition = get_object_or_404(LogDefinition, id=id)
        log_entries = LogEntry.objects.filter(log_definition_id=id).order_by(
            "-timestamp"
        )
        paginator = TableResultSetPagination()
        paginated_log_entries = paginator.paginate_queryset(log_entries, request)
        if paginated_log_entries is None:
            return self.error_response(
                message="No log entries found for this definition",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = LogTableSerializer(paginated_log_entries, many=True)
        response_data = {
            "table_meta": {
                "name": log_definition.name,
                "columns": log_definition.fields,
                "description": log_definition.description,
            },
            "rows": log_entries,
        }

        serializer = LogTableResponseSerializer(response_data)
        return self.success_response(
            serializer.data, message="Log table retrieved successfully"
        )


class LogDefinitionCreateDeleteView(BaseAPIView):
    def post(self, request):
        serializer = LogDefinitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.created_response(
                data=serializer.data, message="Log definition created successfully"
            )
        return self.validation_error_response(serializer.errors)

    def patch(self, request, id):
        log_definition = get_object_or_404(LogDefinition, id=id)
        serializer = LogDefinitionRequestSerializer(
            log_definition, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return self.created_response(
                data=serializer.data, message="Log definition updated successfully"
            )
        return self.validation_error_response(serializer.errors)

    def delete(self, request, id):
        log_definition = get_object_or_404(LogDefinition, id=id)
        # soft delete: mark as inactive instead of deleting
        log_definition.is_deleted = True
        log_definition.deleted_at = timezone.now()
        log_definition.save()
        # TODO: archive all entries of this table
        # implemented in signals: test this
        return self.success_response(message="Log definition deleted successfully")


class LogEntryDetailUpdateDeleteView(BaseAPIView):
    def get_object(self, id):
        return get_object_or_404(LogEntry, id=id)

    def get(self, request, id):
        log_entry = self.get_object(id)
        serializer = LogEntrySerializer(log_entry)
        return self.success_response(
            serializer.data, message="Log entry retrieved successfully"
        )

    def post(self, request, id):
        log_entry = self.get_object(id)
        serializer = LogEntrySerializer(log_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(
                serializer.data, message="Log entry updated successfully"
            )
        return self.validation_error_response(serializer.errors)

    def delete(self, request, id):
        log_entry = self.get_object(id)
        log_entry.is_deleted = True
        log_entry.deleted_at = timezone.now()
        log_entry.save()
        return self.success_response(message="Log entry deleted successfully")

    def patch(self, request, id):
        log_entry = get_object_or_404(LogEntry, id=id)
        serializer = LogEntrySerializer(log_entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.created_response(
                data=serializer.data, message="Log entry updated successfully"
            )
        return self.validation_error_response(serializer.errors)


class ActivityView(BaseAPIView):
    def get(self, request, user_id):
        log_entries = LogEntry.objects.filter(
            log_definition__user__id=user_id
        ).order_by("-created_at")
        serializer = LogEntrySerializer(log_entries, many=True)
        if not serializer:
            return self.not_found_response(serializer.data)
        return self.success_response(
            serializer.data, message="Activity retrieved sucessfully"
        )
