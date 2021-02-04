import base64
from django.core.files.base import ContentFile


def decode_base64(base64_text, file_name):
    file_format, imgstr = base64_text.split(';base64,')
    ext = file_format.split('/')[-1]
    file_decoded = ContentFile(base64.b64decode(
        imgstr), name=f'{file_name}.{ext}')

    return file_decoded
