import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from json_parser.serializers.json_parser import JsonParserSerializer
from json_parser.views.json_parser import JsonParser

logging.basicConfig(format='%(message)s')


class JsonParserView(APIView):
    """
    Convert json input to nested json.
    """

    def post(self, request):
        serializer = JsonParserSerializer(data=request.data)

        if not serializer.is_valid():
            logging.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        parser = JsonParser(
            args=validated_data['args'],
            json_input=validated_data['json_input']
        )

        try:
            parser_response = parser.parse()
        except Exception as ex:
            logging.error(ex.args[0])
            return Response(ex.args[0], status=status.HTTP_400_BAD_REQUEST)

        return Response(parser_response, status=status.HTTP_200_OK)
