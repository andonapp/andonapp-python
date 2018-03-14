class AndonAppException(Exception):
    pass

class AndonBadRequestException(AndonAppException):
    pass

class AndonInternalErrorException(AndonAppException):
    pass

class AndonInvalidRequestException(AndonAppException):
    pass

class AndonResourceNotFoundException(AndonAppException):
    pass

class AndonUnauthorizedRequestException(AndonAppException):
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
