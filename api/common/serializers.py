from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file_base64 = serializers.CharField()
    file_name = serializers.CharField()