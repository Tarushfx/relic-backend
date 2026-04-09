from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.views import BaseAPIView
from logs.serializers.request import (
    LogDefinitionRequestSerializer,
)
from .models import LogDefinition, LogEntry
from .serializers.serializers import (
    LogDefinitionSerializer,
    LogEntrySerializer,
    LogTableSerializer,
    TableResultSetPagination,
)
from .serializers.response import (
    LogDefinitionResponseSerializer,
    LogTableResponseSerializer,
)



class LogTableView(BaseAPIView):
    def get_object(self, id):
        try:
            return get_object_or_404(LogDefinition, id=id)
        except LogEntry.DoesNotExist:
            return None

    def get(self, request, id=None):
        try:
            if id is None:
                definitions = LogDefinition.objects.filter(
                    user=request.user, is_deleted=False
                )
                serializer = LogDefinitionSerializer(definitions, many=True)
                return self.success_response(data=serializer.data)

            log_definition = self.get_object(id)
            if not log_definition or log_definition.is_deleted:
                return self.not_found_response(
                    message="Log definition not found",
                )
            if request.user != log_definition.user:
                return self.unauthorized_response()

            log_entries = LogEntry.objects.filter(log_definition_id=id).order_by(
                "-timestamp"
            )
            paginator = TableResultSetPagination()
            paginated_log_entries = paginator.paginate_queryset(log_entries, request)
            if paginated_log_entries is None:
                return self.error_response(
                    message="No log entries found for this definition"
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
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = LogDefinitionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.created_response(
                    data=serializer.data, message="Log definition created successfully"
                )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id):
        try:
            log_definition = self.get_object(id)
            if not log_definition:
                return self.not_found_response()
            serializer = LogDefinitionRequestSerializer(
                log_definition, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return self.created_response(
                    data=serializer.data, message="Log definition updated successfully"
                )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, id):
        try:
            log_definition = self.get_object(id)
            if not log_definition:
                return self.not_found_response()
            # soft delete: mark as inactive instead of deleting
            log_definition.is_deleted = True
            log_definition.deleted_at = timezone.now()
            log_definition.save()
            return self.success_response(message="Log definition deleted successfully")
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogEntryDetailUpdateDeleteView(BaseAPIView):
    def get_object(self, id):
        try:
            return get_object_or_404(LogEntry, id=id)
        except LogEntry.DoesNotExist:
            return None

    def get(self, request, id):
        try:
            log_entry = self.get_object(id)
            if not log_entry:
                return self.not_found_response()
            serializer = LogEntrySerializer(log_entry)
            return self.success_response(
                serializer.data, message="Log entry retrieved successfully"
            )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, id):
        try:
            log_entry = self.get_object(id)
            if not log_entry:
                return self.not_found_response()
            serializer = LogEntrySerializer(log_entry, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.success_response(
                    serializer.data, message="Log entry updated successfully"
                )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, id):
        try:
            log_entry = self.get_object(id)
            if not log_entry:
                return self.not_found_response()
            log_entry.is_deleted = True
            log_entry.deleted_at = timezone.now()
            log_entry.save()
            return self.success_response(message="Log entry deleted successfully")
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id):
        try:
            log_entry = self.get_object(id)
            if not log_entry:
                return self.not_found_response()
            serializer = LogEntrySerializer(log_entry, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.created_response(
                    data=serializer.data, message="Log entry updated successfully"
                )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ActivityView(BaseAPIView):
    def get(self, request):
        try:
            user_id = request.user.id
            if not user_id:
                return self.unauthorized_response()
            log_entries = LogEntry.objects.filter(
                log_definition__user__id=user_id
            ).order_by("-created_at")
            serializer = LogEntrySerializer(log_entries, many=True)
            if not serializer.data:
                return self.not_found_response(serializer.data)
            return self.success_response(
                serializer.data, message="Activity retrieved sucessfully"
            )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
