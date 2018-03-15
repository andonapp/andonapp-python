import unittest
from andonapp.exceptions import *


class TestExceptions(unittest.TestCase):
    def test_do_nothing_when_null(self):
        raise_from_error_response(None)

    def test_do_nothing_when_type_null(self):
        raise_from_error_response({
            'prop': 'value'
        })

    def test_bad_request_exception(self):
        with self.assertRaisesRegexp(AndonBadRequestException, 'message') as context:
            raise_from_error_response({
                'errorType': 'BAD_REQUEST',
                'errorMessage': 'message'
            })

    def test_invalid_request_exception(self):
        with self.assertRaisesRegexp(AndonInvalidRequestException, 'message') as context:
            raise_from_error_response({
                'errorType': 'INVALID_REQUEST',
                'errorMessage': 'message'
            })

    def test_resource_not_found_exception(self):
        with self.assertRaisesRegexp(AndonResourceNotFoundException, 'message') as context:
            raise_from_error_response({
                'errorType': 'RESOURCE_NOT_FOUND',
                'errorMessage': 'message'
            })

    def test_unauthorized_exception(self):
        with self.assertRaisesRegexp(AndonUnauthorizedRequestException, 'message') as context:
            raise_from_error_response({
                'errorType': 'UNAUTHORIZED_REQUEST',
                'errorMessage': 'message'
            })

    def test_internal_error_exception(self):
        with self.assertRaisesRegexp(AndonInternalErrorException, 'message') as context:
            raise_from_error_response({
                'errorType': 'INTERNAL_ERROR',
                'errorMessage': 'message'
            })

    def test_unknown_error(self):
        with self.assertRaisesRegexp(AndonAppException, 'message') as context:
            raise_from_error_response({
                'errorType': 'ASDF',
                'errorMessage': 'message'
            })

    def test_unauthorized_spring_exception(self):
        with self.assertRaisesRegexp(AndonUnauthorizedRequestException, 'Unauthorized') as context:
            raise_from_error_response({
                    'timestamp': '2018-03-07T16:15:19.033+0000',
                    'status': 401,
                    'error': 'Unauthorized',
                    'message': 'Unauthorized',
                    'path': '/public/api/v1/data/report'
                })

    def test_bad_request_exception_spring(self):
        with self.assertRaisesRegexp(AndonBadRequestException, 'request') as context:
            raise_from_error_response({
                    'timestamp': '2018-03-07T16:15:19.033+0000',
                    'status': 400,
                    'error': 'bad',
                    'message': 'request',
                    'path': '/public/api/v1/data/report'
                })

    def test_raise_internal_error_when_500_code(self):
        with self.assertRaisesRegexp(AndonInternalErrorException, 'error') as context:
            raise_from_error_response({
                    'timestamp': '2018-03-07T16:15:19.033+0000',
                    'status': 500,
                    'error': 'internal',
                    'message': 'error',
                    'path': '/public/api/v1/data/report'
                })
