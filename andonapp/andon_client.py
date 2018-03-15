import requests
from .exceptions import raise_from_error_response
from .exceptions import AndonAppException


class AndonAppClient(object):

    AUTHORIZATION_HEADER = 'Authorization'
    BEARER = 'Bearer '

    DEFAULT_ENDPOINT = 'https://portal.andonapp.com/public/api/v1'
    REPORT_DATA_PATH = '/data/report'
    UPDATE_STATUS_PATH = '/station/update'

    def __init__(self, org_name, api_token):
        self._org_name = org_name
        self._auth_header_value = self.BEARER + api_token
        self.endpoint = self.DEFAULT_ENDPOINT

    def report_data(self, line_name, station_name,
            pass_result, process_time_seconds,
            fail_reason=None, fail_notes=None):
        request = {
            'orgName': self._org_name,
            'lineName': line_name,
            'stationName': station_name,
            'passResult': pass_result,
            'processTimeSeconds': process_time_seconds,
            'failReason': fail_reason,
            'failNotes': fail_notes
        }

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self._auth_header_value
        }

        url = self.endpoint + self.REPORT_DATA_PATH
        response = requests.post(url, json=request, headers=headers)

        if response.status_code != requests.codes.ok:
            self._process_error_response(response)

    def update_station_status(self, line_name, station_name,
            status_color, status_reason=None, status_notes=None):
        request = {
            'orgName': self._org_name,
            'lineName': line_name,
            'stationName': station_name,
            'statusColor': status_color,
            'statusReason': status_reason,
            'statusNotes': status_notes
        }

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self._auth_header_value
        }

        url = self.endpoint + self.UPDATE_STATUS_PATH
        response = requests.post(url, json=request, headers=headers)

        if response.status_code != requests.codes.ok:
            self._process_error_response(response)

    def _process_error_response(self, response):
        raise_from_error_response(response.json())
        raise AndonAppException("Status {}: {}".format(response.status_code, response.text))
