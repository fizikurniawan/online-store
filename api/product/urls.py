from django.conf.urls import url, include
from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet, 'category')
router.register(r'product', ProductViewSet, 'product')

urlpatterns = [
    url(r'', include(router.urls)),
]
