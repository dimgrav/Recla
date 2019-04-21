import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

import recla


class ReclaTest(TestCase):
    """
    Tests for recla.py
    """

    def test_get_opts_args(self):
        """
        Tests parsing of command line options
        """

        opts, args = recla.get_opts_args()
        self.assertEqual(vars(opts), {'lat': None, 'lon': None, 'day_temp': 5800, 'night_temp': 3200})

    def test_api_request(self):
        """
        Tests requesting data from the public API
        """

        api_response = {
            'sunrise': '2019-04-21T05:35:21+00:00',
            'sunset': '2019-04-21T18:57:19+00:00'
        }
        recla.api_request = MagicMock(return_value=api_response)
        results = recla.api_request({'lat': 36.7201600, 'lon': -4.4203400, 'day_temp': 5800, 'night_temp': 3200})
        recla.api_request.assert_called_once()
        self.assertEqual(results, {'sunrise': '2019-04-21T05:35:21+00:00', 'sunset': '2019-04-21T18:57:19+00:00'})

    def test_set_timezone(self):
        """
        Tests setting the timezone to the datetime objects
        """

        naive_results = {'sunrise': '2019-04-21T05:35:21+00:00', 'sunset': '2019-04-21T18:57:19+00:00'}
        aware_results = {
            'sunrise': datetime.datetime(2019, 4, 21, 5, 35, 21, tzinfo=datetime.timezone.utc),
            'sunset': datetime.datetime(2019, 4, 21, 18, 57, 19, tzinfo=datetime.timezone.utc)
        }
        self.assertEqual(recla.set_timezone(naive_results), aware_results)

    @patch('os.popen')
    def test_set_color_temperature(self, popen):
        """
        Tests setting the color temperature
        """

        recla.set_color_temperature(temp=str(5800))
        popen.assert_called_once()

    @patch('recla.set_timezone')
    @patch('recla.api_request')
    def test_refresh(self, set_timezone, api_request):
        """
        Test refreshing the runtime data
        """

        recla.refresh({'lat': None, 'lon': None, 'day_temp': 5800, 'night_temp': 3200})
        set_timezone.assert_called_once()
        api_request.assert_called_once()
