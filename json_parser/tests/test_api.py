import unittest
import base64

from mock import patch, Mock
from rest_framework.test import APIClient


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        super(ApiTestCase, self).setUp()

        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Basic " + base64.b64encode(b"user:pass").decode('ascii'))

    def test_not_secure(self):
        # Given
        self.client.credentials(HTTP_AUTHORIZATION="")

        # When
        response = self.client.post('/api/v1/parse-json/', data={}, secure=True, content_type='application/json')

        # Then
        self.assertEqual(response.status_code, 401)

    def test_method_not_allowed(self):
        # When
        response = self.client.get('/api/v1/parse-json/', data={}, secure=True, content_type='application/json')

        # Then
        self.assertEqual(response.status_code, 405)

    @patch('json_parser.api.logging')
    @patch('json_parser.api.JsonParserSerializer')
    def test_serializer_error(self, mock_serializer, mock_logging):
        # Given
        mock_instance = Mock(errors={
            'args': ['This field is required.'],
            'json_input': ['This field is required.']
        })
        mock_instance.is_valid.return_value = False
        mock_serializer.return_value = mock_instance

        # When
        response = self.client.post('/api/v1/parse-json/', data={}, secure=True, content_type='application/json')

        # Then
        mock_logging.error.assert_called_once_with({
            'args': ['This field is required.'],
            'json_input': ['This field is required.']
        })
        self.assertEqual(response.status_code, 400)

    @patch('json_parser.api.JsonParser')
    @patch('json_parser.api.logging')
    @patch('json_parser.api.JsonParserSerializer')
    def test_parser_error(self, mock_serializer, mock_logging, mock_json_parser):
        # Given
        mock_instance = Mock(validated_data={'args': [], 'json_input': []})
        mock_instance.is_valid.return_value = True
        mock_serializer.return_value = mock_instance

        mock_parser = Mock()
        mock_parser.parse.side_effect = Exception('Error message')
        mock_json_parser.return_value = mock_parser

        # When
        response = self.client.post('/api/v1/parse-json/', data={}, secure=True,
                                    content_type='application/json')

        # Then
        mock_logging.error.assert_called_once_with('Error message')
        self.assertEqual(response.status_code, 400)

    @patch('json_parser.api.JsonParser')
    @patch('json_parser.api.JsonParserSerializer')
    def test_success(self, mock_serializer, mock_json_parser):
        # Given
        mock_instance = Mock(validated_data={'args': [], 'json_input': []})
        mock_instance.is_valid.return_value = True
        mock_serializer.return_value = mock_instance

        mock_parser = Mock()
        expected_response = [{
            "FR": {
                "Lyon": [
                    {
                        "currency": "EUR",
                        "amount": 11.4
                    }
                ]
            }
        }]
        mock_parser.parse.return_value = expected_response
        mock_json_parser.return_value = mock_parser

        # When
        response = self.client.post('/api/v1/parse-json/', data={}, secure=True,
                                    content_type='application/json')

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)
