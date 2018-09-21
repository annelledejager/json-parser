import unittest

from mock import patch

from json_parser.views.json_parser import JsonParser


class ViewTestCase(unittest.TestCase):
    def setUp(self):
        super(ViewTestCase, self).setUp()

        self.json = [{
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        }, {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        }, {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        }]

    def test_no_args(self):
        # Given
        parser = JsonParser([], self.json)

        # When
        result = parser.parse()

        # Then
        self.assertEqual(result, self.json)

    @patch('json_parser.views.json_parser.logging')
    def test_invalid_arg(self, mock_logging):
        # Given
        parser = JsonParser(['invalid_arg'], self.json)

        # When
        with self.assertRaises(Exception) as ex:
            parser.parse()

        # Then
        mock_logging.error.assert_called_once_with('Key does not exist in json input')

    def test_no_json(self):
        # Given
        parser = JsonParser(['currency'], {})

        # When
        result = parser.parse()

        # Then
        self.assertEqual(result, [])

    @patch('json_parser.views.json_parser.logging')
    def test_invalid_json(self, mock_logging):
        # Given
        parser = JsonParser(['currency'], str(self.json))

        # When
        with self.assertRaises(Exception) as ex:
            parser.parse()

        # Then
        mock_logging.error.assert_called_once_with('Incorrect input type')

    def test_success(self):
        # Given
        parser = JsonParser(['country', 'city'], self.json)

        # When
        result = parser.parse()

        # Then
        self.assertEqual(result, [
            {
                "US": {
                    "Boston": [
                        {
                            "currency": "USD",
                            "amount": 100
                        }
                    ]
                }
            },
            {
                "FR": {
                    "Paris": [
                        {
                            "currency": "EUR",
                            "amount": 20
                        }
                    ]
                }
            },
            {
                "FR": {
                    "Lyon": [
                        {
                            "currency": "EUR",
                            "amount": 11.4
                        }
                    ]
                }
            }
        ])
