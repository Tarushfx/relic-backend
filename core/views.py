from rest_framework import views
from .responses import ApiResponse


class BaseAPIView(views.APIView):
    """
    Base API view that provides standardized response methods.
    All views should inherit from this instead of APIView directly.
    """

    def unauthorized_response(self, message="Authentication required"):
        """Return a standardized unauthorized response."""
        return ApiResponse.unauthorized(message=message)

    def success_response(
        self, data=None, message="Operation successful", status_code=200
    ):
        """Return a standardized success response."""
        return ApiResponse.success(data=data, message=message, status_code=status_code)

    def error_response(self, message="An error occurred", errors=None, status_code=400):
        """Return a standardized error response."""
        return ApiResponse.error(
            message=message, errors=errors, status_code=status_code
        )

    def created_response(self, data=None, message="Resource created successfully"):
        """Return a standardized created response."""
        return ApiResponse.created(data=data, message=message)

    def validation_error_response(self, errors, message="Validation failed"):
        """Return a standardized validation error response."""
        return ApiResponse.validation_error(errors=errors, message=message)

    def not_found_response(self, message="Resource not found"):
        """Return a standardized not found response."""
        return ApiResponse.not_found(message=message)

    def malformed_request(self, errors=None, message="Malformed request"):
        """Return a standardized malformed request response."""
        return ApiResponse.error(errors, message)
