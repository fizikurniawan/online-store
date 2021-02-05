from django.conf.urls import url, include
from rest_framework import routers

from .views import UploadFileViewSet

router = routers.DefaultRouter()
router.register(r'upload', UploadFileViewSet, 'upload')

urlpatterns = [
    url(r'^authentication/', include('api.authentication.urls',)),
    url(r'^product/', include('api.product.urls',)),
    url(r'^common/', include(router.urls))
]
