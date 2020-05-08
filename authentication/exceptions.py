from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    # if exception is not defined here, declare DEFAULT handler method

    response = exception_handler(exc, context)
    handlers = {
        'ProfileDoesNotExist': _handle_generic_error,
        'ValidationError': _handle_generic_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # if this exception is one that is defined, handle it, otherwise, return the respone granted earlier by the DEFAULT exception

        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):

    response.data = {
        'errors': response.data
    }

    return response