#!/usr/bin/env python3
import datetime
import json
import os
import sys
from copy import deepcopy

import requests
from dateutil import tz

from lib.errors import *
from lib.options import ReclaOptionParser, OptionError

__author__ = "Dimitris Gravanis"
__copyright__ = "2019"
__version__ = "0.0.1"
__description__ = "Recla: easy on the eyes!"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


def get_opts_args():
    """
    Retrieve command line options and arguments

    :return: lists of options/arguments
    """

    usage = 'python %prog [options]'

    parser = ReclaOptionParser(usage=usage, version=__version__, description=__description__)
    parser.add_option('-z', '--lat', help='Latitude value', default=None)
    parser.add_option('-y', '--lon', help='Longitude value', default=None)
    parser.add_option('-d', '--day_temp', help='Day time color temperature', default=5800)
    parser.add_option('-n', '--night_temp', help='Night time color temperature', default=3200)

    return parser.parse_args()


def exit_with_error(error: str):
    """
    Exit with an error message

    :param error: the error message string
    :return: nothing
    """

    print(error)
    sys.exit(2)


def api_request(options: dict):
    """
    Perform an HTTP GET request to https://api.sunrise-sunset.org/
    - Request a JSON response
    - Receive sunrise/sunset times in 'YYYY:MM:DDTHH:MM:SS+HH:MM' format

    :param options: the command line options dictionary
    :return: the sunrise/sunset string values
    """

    lat, lon = None, None
    try:
        lat = float(options['lat'] if 'lat' in options else options['z'])
        lon = float(options['lon'] if 'lon' in options else options['y'])
    except ValueError:
        exit_with_error(CoordinateError.message)

    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date=today&formatted=0'
    api_response = requests.get(url=url)

    json_response = None
    if api_response:
        json_response = json.loads(api_response.content)
    else:
        exit_with_error(APIResponseError.message)

    try:
        return {
            'sunrise': json_response['results']['sunrise'],
            'sunset': json_response['results']['sunset']
        }
    except KeyError:
        exit_with_error(APIResultsError.message)


def set_timezone(results: dict):
    """
    Make sunrise/sunset string values timezone-aware datetime objects
    - Include daylight saving time (DST)

    :param results: the API request results
    :return: dictionary of sunrise/sunset datetime objects
    """

    tz_string = datetime.datetime.now(tz=datetime.timezone.utc).astimezone().tzname()
    tz_obj = tz.gettz(tz_string)

    results_copy = deepcopy(results)
    for k in results_copy:
        res_parts = results_copy[k].split("+")
        res_parts[-1] = tz_string
        results_copy[k] = datetime.datetime.strptime('+'.join(res_parts), '%Y-%m-%dT%H:%M:%S+%Z').replace(tzinfo=datetime.timezone.utc).astimezone(tz=tz_obj)

    return results_copy


def set_color_temperature(options: dict):
    """
    Set the screen color temperature

    :param options: the command line options dictionary
    :return: nothing
    """

    temp = options['day_temp'] if 'day_temp' in options else options['d']
    if not all(char.isdigit() for char in temp):
        exit_with_error(TemperatureError.message)

    os.popen(f'{__abs_dirpath__}/sct/rsct {temp}')


if __name__ == '__main__':
    opts, args = None, None
    try:
        opts, args = get_opts_args()
    except OptionError as e:
        exit_with_error(str(e))

    if opts:
        opts_dict = vars(opts)
        time_results = api_request(options=opts_dict)
        dt_time_results = set_timezone(results=time_results)
        set_color_temperature(options=opts_dict)
