from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats all errors in a consistent JSON structure.
    """
    response = exception_handler(exc, context)

    if response is not None:
        message = "An error occurred"
        if hasattr(exc, "detail") and exc.detail:
            message = exc.detail
        elif isinstance(response.data, dict):
            message = response.data.get("detail", response.data.get("message", message))
        elif isinstance(response.data, list):
            message = "Validation failed"

        response.data = {
            "success": False,
            "code": response.status_code,
            "message": message,
            "data": None,
            "errors": response.data,
        }

    return response
