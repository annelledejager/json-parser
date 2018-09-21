import unittest

from json_parser.serializers.json_parser import JsonParserSerializer


class SerializersTestCase(unittest.TestCase):
    def setUp(self):
        super(SerializersTestCase, self).setUp()

    def test_missing_args(self):
        # Given
        data = {
            'json_input': {},
        }

        # When
        serializer = JsonParserSerializer(data=data)

        # Then
        self.assertFalse(serializer.is_valid())

    def test_missing_json_input(self):
        # Given
        data = {
            'args': [],
        }

        # When
        serializer = JsonParserSerializer(data=data)

        # Then
        self.assertFalse(serializer.is_valid())

    def test_missing_inputs(self):
        # When
        serializer = JsonParserSerializer(data={})

        # Then
        self.assertFalse(serializer.is_valid())

    def test_success(self):
        # Given
        data = {
            'args': [],
            'json_input': {},
        }

        # When
        serializer = JsonParserSerializer(data=data)

        # Then
        self.assertTrue(serializer.is_valid())
