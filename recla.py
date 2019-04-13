import datetime
import getopt
import json
import os
import sys
from copy import deepcopy

import requests
from dateutil import tz

__author__ = "Dimitris Gravanis"
__copyright__ = "2019"
__version__ = "0.0.1"
__description__ = "Recla: easy on the eyes!"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


errors = {
    'NOT_INT': 'Temperature value(s) must be integers',
    'NOT_FLOAT': 'Latitude/Longitude value(s) must be floating point numbers',
    'NO_RESPONSE': 'API Response not available',
    'NO_CONTENT': 'API Response content not available',
    'NO_RESULTS': 'API sunrise/sunset results not available'
}


def get_opts_args():
    """
    Retrieve command line options and arguments

    :return: lists of options/arguments
    """

    return getopt.getopt(
        args=sys.argv[1:],
        shortopts="z:y:d:n:",
        longopts=["lat=", "lon=", "day_temp=", "night_temp="]
    )


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
    - Receive sunrise/sunset times in 'YYYY:MM:DDTHH:MM:SS+HH:MM' format

    :param options: the command line options
    :return: the sunrise/sunset string values
    """

    lat, lng = None, None
    try:
        lat = float(options[0][1])
        lng = float(options[1][1])
    except ValueError:
        exit_with_error(error=errors['NOT_FLOAT'])

    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date=today&formatted=0'
    api_response = requests.get(url=url)

    json_response = None
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
    - Include daylight saving time (DST)

    :param results: the API request results
    :return: dictionary of sunrise/sunset datetime objects
    """

    tz_string = datetime.datetime.now(tz=datetime.timezone.utc).astimezone().tzname()
    tz_obj = tz.gettz(tz_string)

    results_copy = deepcopy(results)
    for k in results_copy:
        res_parts = results_copy[k].split("+")
        res_parts.pop(-1)
        res_parts.append(tz_string)
        results_copy[k] = '+'.join(res_parts)
        results_copy[k] = datetime.datetime.strptime('+'.join(res_parts), '%Y-%m-%dT%H:%M:%S+%Z').replace(tzinfo=datetime.timezone.utc).astimezone(tz=tz_obj)

    return results_copy


def set_color_temperature(temp: str):
    """
    Set the screen color temperature

    :param temp: the color temperature
    :return: nothing
    """

    if not all(char.isdigit() for char in temp):
        exit_with_error(error=errors['NOT_INT'])

    os.popen(f'{__abs_dirpath__}/sct/rsct {temp}')


if __name__ == '__main__':
    opts, args = None, None
    try:
        opts, args = get_opts_args()
    except getopt.GetoptError as e:
        exit_with_error(str(e))

    if opts and 0 < len(opts) <= 4:
        time_results = api_request(opts)
        dt_time_results = set_timezone(results=time_results)
        set_color_temperature(opts[2][1])
