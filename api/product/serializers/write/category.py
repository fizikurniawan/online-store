from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet, mixins

from api.common.models import File


class CategoryWriteSerializer(serializers.Serializer):
    file_uuid = serializers.CharField()
    display_name = serializers.CharField()

    def validate(self, data):
        file_uuid = data.pop('file_uuid')

        file_instance = File.objects.filter(
            uuid=file_uuid
        )

        if not file_instance.exists():
            raise serializers.ValidationError({
                'file_uuid': 'File UUID invalid'
            })

        data['file'] = file_instance.last()
        return data
