"""
Packages custom Andon exceptions.
"""

class AndonAppException(Exception):
    """
    Generic catch-all exception when a request to Andon fails.
    """
    pass

class AndonBadRequestException(AndonAppException):
    """
    Generic exception when a request to Andon fails because there's something
    wrong with the request.
    """
    pass

class AndonInternalErrorException(AndonAppException):
    """
    Generic exception when a request to Andon fails because there's something
    wrong within Andon.
    """
    pass

class AndonInvalidRequestException(AndonAppException):
    """
    Exception when a request to Andon fails because one of the inputs is invalid.
    """
    pass

class AndonResourceNotFoundException(AndonAppException):
    """
    Exception when a request to Andon fails because a referenced resource
    (such as a station) can't be found in the system.
    """
    pass

class AndonUnauthorizedRequestException(AndonAppException):
    """
    Exception when a request to Andon fails because it's unauthorized.
    """
    pass

def raise_from_error_response(response):
    if not response:
        return

    if 'errorType' in response:
        error_type = response['errorType']
        message = response['errorMessage']

        if "BAD_REQUEST" == error_type:
            raise AndonBadRequestException(message)
        elif "INVALID_REQUEST" == error_type:
            raise AndonInvalidRequestException(message)
        elif "RESOURCE_NOT_FOUND" == error_type:
            raise AndonResourceNotFoundException(message)
        elif "UNAUTHORIZED_REQUEST" == error_type:
            raise AndonUnauthorizedRequestException(message)
        elif "INTERNAL_ERROR" == error_type:
            raise AndonInternalErrorException(message)
        else:
            raise AndonAppException(message)

    if 'status' in response:
        status = response['status']
        message = response['message']

        if 401 == status:
            raise AndonUnauthorizedRequestException(message)
        elif status >= 400 and status < 500:
            raise AndonBadRequestException(message)
        else:
            raise AndonInternalErrorException(message)
