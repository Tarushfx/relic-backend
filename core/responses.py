from rest_framework.response import Response
from rest_framework import status


class ApiResponse:
    """Standardized API response utility for consistent JSON formatting."""

    @staticmethod
    def success(
        data=None, message="Operation successful", status_code=status.HTTP_200_OK
    ):
        """Create a success response."""
        return Response(
            {
                "success": True,
                "code": status_code,
                "message": message,
                "data": data,
                "errors": None,
            },
            status=status_code,
        )

    @staticmethod
    def error(
        message="An error occurred",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        """Create an error response."""
        return Response(
            {
                "success": False,
                "code": status_code,
                "message": message,
                "data": None,
                "errors": errors,
            },
            status=status_code,
        )

    @staticmethod
    def created(data=None, message="Resource created successfully"):
        """Create a resource created response."""
        return ApiResponse.success(
            data=data, message=message, status_code=status.HTTP_201_CREATED
        )

    @staticmethod
    def no_content(message="No content"):
        """Create a no content response."""
        return ApiResponse.success(
            data=None, message=message, status_code=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def unauthorized(message="Authentication required"):
        """Create an unauthorized response."""
        return ApiResponse.error(
            message=message, status_code=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def forbidden(message="Permission denied"):
        """Create a forbidden response."""
        return ApiResponse.error(message=message, status_code=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def not_found(message="Resource not found"):
        """Create a not found response."""
        return ApiResponse.error(message=message, status_code=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def validation_error(errors, message="Validation failed"):
        """Create a validation error response."""
        return ApiResponse.error(
            message=message, errors=errors, status_code=status.HTTP_400_BAD_REQUEST
        )
