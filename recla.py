#!/usr/bin/python3

import datetime
import json
import os
import sys
import getopt

import requests


errors = {
    'NO_RESPONSE': 'API Response not available',
    'NO_CONTENT': 'API Response content not available',
    'NO_RESULTS': 'API sunrise/sunset results not available'
}


def exit_with_error(error: str):
    """
    Exit with an error message

    :param error: the error message string
    :return: nothing
    """
    print(error)
    sys.exit(2)


def api_request(options: list):
    """
    Perform an HTTP GET request to https://api.sunrise-sunset.org/
    - Request a JSON response
    - Get sunrise and sunset data in datetime object format

    :param options: the command line options
    :return: the sunrise/sunset datetime values
    """

    json_response = None

    lat = options[0][1]  # 39.63636488778663
    lng = options[1][1]  # 22.426786422729492

    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date=today&formatted=0'
    api_response = requests.get(url=url)

    if api_response:
        json_response = json.loads(api_response.content)
    else:
        exit_with_error(error=errors['NO_RESPONSE'])

    try:
        return {
            'sunrise': json_response['results']['sunrise'],
            'sunset': json_response['results']['sunset']
        }
    except KeyError:
        exit_with_error(error=errors['NO_RESULTS'])


def set_timezone(results: dict):
    """
    Make sunrise/sunset string values timezone-aware datetime objects

    :param results: the API request results
    :return: the sunrise/sunset datetime objects
    """

    pass


def set_color_temperature(temp: int):
    """
    Set the screen color temperature

    :param temp: the color temperature
    :return:
    """

    pass


if __name__ == '__main__':
    opts, args = None, None

    try:
        opts, args = getopt.getopt(
            args=sys.argv[1:],
            shortopts="z:y:d:n:",
            longopts=["lat=", "lon=", "day_temp=", "night_temp="]
        )
    except getopt.GetoptError as e:
        exit_with_error(str(e))

    if opts and len(opts) > 0:
        time_results = api_request(opts)
