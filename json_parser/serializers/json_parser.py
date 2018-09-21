from rest_framework import serializers


class JsonParserSerializer(serializers.Serializer):
    args = serializers.ListField(required=True)
    json_input = serializers.JSONField(required=True)
