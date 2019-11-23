from django import http
from rest_framework import exceptions
from rest_framework.views import exception_handler
import logging

_LOGGER = logging.getLogger("GlobalException")


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if not response:
        return None
    _LOGGER.exception("Got an unhandled exception")
    # If the exception is an APIException, we set the full details
    # The only exception is for Validation errors, to prevent an overly complicated returned object
    if isinstance(exc, exceptions.APIException) and not isinstance(exc, exceptions.ValidationError):
        response.data = exc.get_full_details()
        try:
            response.status_code = int(exc.get_codes())
        except ValueError:
            pass
        old_response = response
        response = http.JsonResponse(response.data, status=response.status_code)
        response.data = old_response.data
        response.status_code = old_response.status_code
    return response


class HandleExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_exception(self, request, exception):  # pylint: disable=no-self-use
        return custom_exception_handler(exception, request)

    def __call__(self, request):
        response = self.get_response(request)
        return response
