from math import log

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.views import BaseAPIView
from logs.pagination import ActivityResultSetPagination
from logs.serializers.request import (
    LogDefinitionRequestSerializer,
    LogEntryRequestSerializer,
)
from .models import LogDefinition, LogEntry
from .serializers.serializers import (
    LogDefinitionSerializer,
    LogEntrySerializer,
    LogTableSerializer,
)
from .pagination import TableResultSetPagination
from .serializers.response import (
    ActivityResponseSerializer,
    LogDefinitionResponseSerializer,
    LogTableResponseSerializer,
)


class LogTableView(BaseAPIView):
    def get_object(self, id):
        return LogEntry.objects.filter(id=id).first()

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
                "rows": paginated_log_entries,
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
            user = request.user
            if not user:
                return self.unauthorized_response()
            serializer = LogDefinitionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return self.created_response(
                    data=serializer.data, message="Log definition created successfully"
                )
            return self.malformed_request(serializer.errors)
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id):
        return self.http_method_not_allowed(request)
        #  TODO: implement later
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
            return self.malformed_request(serializer.errors)
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, id):
        try:
            log_definition = self.get_object(id)
            if not log_definition or log_definition.is_deleted:
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
        return LogEntry.objects.filter(id=id).first()

    def get_table(self, id):
        return LogDefinition.objects.filter(id=id).first()

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
            log_definition = self.get_table(id)
            if not log_definition or log_definition.is_deleted:
                return self.not_found_response("No Table found")
            if request.user != log_definition.user:
                return self.unauthorized_response()
            serializer = LogEntryRequestSerializer(
                data=request.data, context={"log_definition": log_definition}
            )
            if serializer.is_valid():
                serializer.save(log_definition=log_definition)
                return self.success_response(
                    serializer.data, message="Log entry updated successfully"
                )
            return self.malformed_request(serializer.errors)
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
            if not log_entry or log_entry.is_deleted:
                return self.not_found_response()
            if not log_entry.log_definition:
                return self.malformed_request(message="No table found")
            if log_entry.log_definition.user != request.user:
                return self.unauthorized_response()
            serializer = LogEntrySerializer(log_entry, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.created_response(
                    data=serializer.data, message="Log entry updated successfully"
                )
            return self.malformed_request(serializer.errors)
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ActivityView(BaseAPIView):
    def get(self, request):
        try:
            user = request.user
            if not user:
                return self.unauthorized_response()
            log_entries = LogEntry.objects.filter(
                log_definition__user=user,
                is_deleted=False,
            ).order_by("-timestamp")
            paginator = ActivityResultSetPagination()
            page = paginator.paginate_queryset(log_entries, request)
            if not page:
                return self.not_found_response()
            serializer = ActivityResponseSerializer(page, many=True)
            return self.success_response(
                paginator.get_paginated_response(serializer.data),
                message="Activity retrieved sucessfully",
            )
        except Exception as e:
            return self.error_response(
                str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
