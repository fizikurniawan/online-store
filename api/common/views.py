from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from api.common.models import File
from libs.base64 import decode_base64

from .serializers import FileUploadSerializer


class UploadFileViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = FileUploadSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_base64 = serializer.validated_data.get('file_base64')
        file_name = serializer.validated_data.get('file_name')

        file_object = decode_base64(file_base64, file_name)
        file_instance = File.objects.create(
            display_name=file_name, file=file_object)

        return Response({
            'status': 'success',
            'message': 'Success upload file',
            'data': {
                'uuid': file_instance.uuid
            }
        })
