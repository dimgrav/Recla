__author__ = "Dimitris Gravanis"
__copyright__ = "2019"
__version__ = "0.0.1"
__description__ = "Recla errors"


class TemperatureError(Exception):
    """
    Raise on temperature value errors
    """

    message = 'Temperature value(s) must be integers'


class CoordinateError(Exception):
    """
    Raise on coordinate value errors
    """

    message = 'Latitude/Longitude value(s) must be floating point numbers'


class APIResponseError(Exception):
    """
    Raise on API response error
    """

    message = 'API Response not available'


class APIResultsError(Exception):
    """
    Raise on api response result error
    """

    message = 'API sunrise/sunset results not available'
