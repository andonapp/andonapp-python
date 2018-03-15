**********************
AndonApp Python Client
**********************

Python client library for reporting data to `Andon <https://www.andonapp.com/>`_

=======
Install
=======

.. code-block::

    pip install andonapp

=====
Usage
=====

In order to programmatically connect to Andon's APIs you must first generate an API token. This is done by logging into your Andon account, navigating to the `API settings page <https://portal.andonapp.com/settings/tokens>`_, and generating a new token.  Make sure to record the token, and keep it secret.

Reference Andon's `getting started guide <https://drive.google.com/file/d/0B5cQI3VvgCT8UllmaENIazlwbGc/view>`_ and `API guide <https://drive.google.com/file/d/0B5cQI3VvgCT8enNIZGN2QVo0STg/view>`_ for complete details on these prerequisites

Setting up the Client
=====================

Now that you have a token, create a client as follows:

.. code-block:: python

    from andonapp import AndonAppClient

    client = AndonAppClient(org_name, api_token)

Reporting Data
==============

Here's an example of using the client to report a success:

.. code-block:: python

    client.report_data(
        line_name='line 1',
        station_name='station 1',
        pass_result='PASS',
        process_time_seconds=100)

And a failure:

.. code-block:: python

    client.report_data(
        line_name='line 1',
        station_name='station 1',
        pass_result='FAIL',
        process_time_seconds=100,
        fail_reason='Test Failure',
        fail_notes='notes')

Updating a Station Status
=========================

Here's an example of flipping a station to Red:

.. code-block:: python

    client.update_station_status(
        line_name='line 1',
        station_name='station 1',
        status_color='RED',
        status_reason='Missing parts',
        status_notes='notes')

And back to Green:

.. code-block:: python

    client.update_station_status(
        line_name='line 1',
        station_name='station 1',
        status_color='GREEN')

=======
License
=======

`Licensed under the MIT license <LICENSE>`_.
