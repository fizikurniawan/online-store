from rest_framework import serializers
from libs.base64 import decode_base64


class FileUploadSerializer(serializers.Serializer):
    file_base64 = serializers.CharField()
    file_name = serializers.CharField()

    def validate(self, data):
        file_base64 = data.get('file_base64')
        file_name = data.get('file_name')

        try:
            decode_base64(file_base64, file_name)
        except:
            raise serializers.ValidationError({
                'file_base64': 'invalid base64'
            })

        return data