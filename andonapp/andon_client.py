"""
Client for making requests to Andon (www.andonapp.com). In order to use the
client you must generate an API token on the org settings page within Andon.

Example
-------
.. highlight:: python
    client = AndonAppClient('orgName', 'apiToken')
    client.report_data(line_name='line 1',
            station_name='station 1',
            pass_result='PASS',
            process_time_seconds=120)
"""

import requests
from .exceptions import raise_from_error_response
from .exceptions import AndonAppException


class AndonAppClient(object):
    """
    Client for making requests to Andon (www.andonapp.com). In order to use the
    client you must generate an API token on the org settings page within Andon.

    Example
    -------
    .. code-block:: python

        client = AndonAppClient('orgName', 'apiToken')
        client.report_data(
                line_name='line 1',
                station_name='station 1',
                pass_result='PASS',
                process_time_seconds=120)

    Parameters
    ----------
    org_name : str
        Organization name within Andon
    api_token : str
        Andon API token necessary to make requests
    """

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
        """
        Reports the outcome of a process at a station to Andon.

        Example
        -------
        .. code-block:: python

            client.report_data(
                    line_name='line 1',
                    station_name='station 1',
                    pass_result='FAIL',
                    process_time_seconds=120,
                    fail_reason='Test Failure',
                    fail_notes='notes')

        Parameters
        ----------
        line_name : str
            The name of the line the station is on
        station_name : str
            The name of the station
        pass_result : str
            The outcome -- must be 'PASS' or 'FAIL'
        process_time_seconds : int
            Total time in seconds spent processing
        fail_reason : str, optional
            If the process failed, the reason why
        fail_notes : str, optional
            If the process failed, additional details on why

        Raises
        ------
        AndonAppException
            If there is a general request failure
        AndonBadRequestException
            If there is something wrong with the request
        AndonInternalErrorException
            If there is a failure within Andon
        AndonInvalidRequestException
            If there are invalid request arguments
        AndonResourceNotFoundException
            If a referenced station can't be found
        AndonUnauthorizedRequestException
            If authorization fails
        """
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
        """
        Changes the status of a station in Andon.

        Example
        -------
        .. code-block:: python

            client.update_station_status(
                    line_name='line 1',
                    station_name='station 1',
                    status_color='YELLOW',
                    status_reason='Missing parts',
                    status_notes='notes')

        Parameters
        ----------
        line_name : str
            The name of the line the station is on
        station_name : str
            The name of the station
        status_color : str
            The color to change the station to -- must be 'GREEN', 'YELLOW', or 'RED'
        status_reason : int, optional
            The reason for the color change
        status_notes : str, optional
            Notes on the change

        Raises
        ------
        AndonAppException
            If there is a general request failure
        AndonBadRequestException
            If there is something wrong with the request
        AndonInternalErrorException
            If there is a failure within Andon
        AndonInvalidRequestException
            If there are invalid request arguments
        AndonResourceNotFoundException
            If a referenced station can't be found
        AndonUnauthorizedRequestException
            If authorization fails
        """
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
