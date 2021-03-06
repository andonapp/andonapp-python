import unittest
from unittest.mock import patch
from andonapp import AndonAppClient
from andonapp.exceptions import *


class TestAndonClient(unittest.TestCase):
    def setUp(self):
        self.endpoint = 'https://portal.andonapp.com/public/api/v1'
        self.report_data_url = self.endpoint + '/data/report'
        self.update_status_url = self.endpoint + '/station/update'

        self.org_name = 'Demo'
        self.api_token = 'api-token'

        self.client = AndonAppClient(self.org_name, self.api_token)

        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer ' + self.api_token
        }

    @patch('requests.post')
    def test_report_data_when_valid_pass_request(self, mock_post):
        self._expect_post(mock_post, 200, {})

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'passResult': 'PASS',
            'processTimeSeconds': 100,
            'failReason': None,
            'failNotes': None
        }

        self.client.report_data(line_name=request['lineName'],
                station_name=request['stationName'],
                pass_result=request['passResult'],
                process_time_seconds=request['processTimeSeconds'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_report_data_when_valid_fail_request(self, mock_post):
        self._expect_post(mock_post, 200, {})

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'passResult': 'PASS',
            'processTimeSeconds': 200,
            'failReason': 'Test Failure',
            'failNotes': 'notes'
        }

        self.client.report_data(line_name=request['lineName'],
                station_name=request['stationName'],
                pass_result=request['passResult'],
                process_time_seconds=request['processTimeSeconds'],
                fail_reason=request['failReason'],
                fail_notes=request['failNotes'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_fail_report_data_when_missing_line_name(self, mock_post):
        self._expect_post(mock_post, 400, {
                'errorType': 'INVALID_REQUEST',
                'errorMessage': 'lineName may not be empty'
            })

        request = {
            'orgName': self.org_name,
            'lineName': None,
            'stationName': 'station 1',
            'passResult': 'PASS',
            'processTimeSeconds': 100,
            'failReason': None,
            'failNotes': None
        }

        with self.assertRaises(AndonInvalidRequestException) as context:
            self.client.report_data(line_name=request['lineName'],
                    station_name=request['stationName'],
                    pass_result=request['passResult'],
                    process_time_seconds=request['processTimeSeconds'],
                    fail_reason=request['failReason'],
                    fail_notes=request['failNotes'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_fail_report_data_when_station_not_found(self, mock_post):
        self._expect_post(mock_post, 400, {
                'errorType': 'RESOURCE_NOT_FOUND',
                'errorMessage': 'Station not found.'
            })

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'passResult': 'PASS',
            'processTimeSeconds': 100,
            'failReason': None,
            'failNotes': None
        }

        with self.assertRaises(AndonResourceNotFoundException) as context:
            self.client.report_data(line_name=request['lineName'],
                    station_name=request['stationName'],
                    pass_result=request['passResult'],
                    process_time_seconds=request['processTimeSeconds'],
                    fail_reason=request['failReason'],
                    fail_notes=request['failNotes'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_fail_report_data_when_invalid_pass_result(self, mock_post):
        self._expect_post(mock_post, 400, {
                'errorType': 'INVALID_REQUEST',
                'errorMessage': "'PAS' is not a valid pass result."
            })

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'passResult': 'PAS',
            'processTimeSeconds': 100,
            'failReason': None,
            'failNotes': None
        }

        with self.assertRaises(AndonInvalidRequestException) as context:
            self.client.report_data(line_name=request['lineName'],
                    station_name=request['stationName'],
                    pass_result=request['passResult'],
                    process_time_seconds=request['processTimeSeconds'],
                    fail_reason=request['failReason'],
                    fail_notes=request['failNotes'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_fail_report_data_when_unauthorized(self, mock_post):
        self._expect_post(mock_post, 401, {
                'timestamp': '2018-03-07T16:15:19.033+0000',
                'status': 401,
                'error': 'Unauthorized',
                'message': 'Unauthorized',
                'path': '/public/api/v1/data/report'
            })

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'passResult': 'PASS',
            'processTimeSeconds': 100,
            'failReason': None,
            'failNotes': None
        }

        with self.assertRaises(AndonUnauthorizedRequestException) as context:
            self.client.report_data(line_name=request['lineName'],
                    station_name=request['stationName'],
                    pass_result=request['passResult'],
                    process_time_seconds=request['processTimeSeconds'],
                    fail_reason=request['failReason'],
                    fail_notes=request['failNotes'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_fail_report_data_when_unknown_failure(self, mock_post):
        self._expect_post(mock_post, 404, {})

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'passResult': 'PASS',
            'processTimeSeconds': 100,
            'failReason': None,
            'failNotes': None
        }

        with self.assertRaises(AndonAppException) as context:
            self.client.report_data(line_name=request['lineName'],
                    station_name=request['stationName'],
                    pass_result=request['passResult'],
                    process_time_seconds=request['processTimeSeconds'],
                    fail_reason=request['failReason'],
                    fail_notes=request['failNotes'])

        self._assert_post_called(mock_post, self.report_data_url, request)

    @patch('requests.post')
    def test_update_station_status_success(self, mock_post):
        self._expect_post(mock_post, 200, {})

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'statusColor': 'YELLOW',
            'statusReason': 'Missing Parts',
            'statusNotes': 'notes'
        }

        self.client.update_station_status(line_name=request['lineName'],
                station_name=request['stationName'],
                status_color=request['statusColor'],
                status_reason=request['statusReason'],
                status_notes=request['statusNotes'])

        self._assert_post_called(mock_post, self.update_status_url, request)

    @patch('requests.post')
    def test_update_station_status_to_green_when_valid(self, mock_post):
        self._expect_post(mock_post, 200, {})

        request = {
            'orgName': self.org_name,
            'lineName': 'line 1',
            'stationName': 'station 1',
            'statusColor': 'GREEN',
            'statusReason': None,
            'statusNotes': None
        }

        self.client.update_station_status(line_name=request['lineName'],
                station_name=request['stationName'],
                status_color=request['statusColor'],
                status_reason=request['statusReason'],
                status_notes=request['statusNotes'])

        self._assert_post_called(mock_post, self.update_status_url, request)

    def _expect_post(self, mock, status_code, response):
        mock.return_value.status_code = status_code
        mock.return_value.json = lambda: response

    def _assert_post_called(self, mock, url, request):
        mock.assert_called_with(url, json=request, headers=self.headers)
