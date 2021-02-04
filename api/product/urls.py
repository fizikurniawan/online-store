from django.conf.urls import url, include
from rest_framework import routers
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet, 'category')

urlpatterns = [
    url(r'', include(router.urls)),
]
