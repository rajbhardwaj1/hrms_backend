from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        logger.error(f"API Error: {exc}")
        response.data = {
            "error": True,
            "message": response.data
        }
    else:
        logger.exception("Unhandled exception")
        return Response(
            {"error": True, "message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
