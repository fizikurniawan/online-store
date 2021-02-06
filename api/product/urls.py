from django.conf.urls import url, include
from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet, ProductFlashSaleViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet, 'category')
router.register(r'product', ProductViewSet, 'product')
router.register(r'flash-sale', ProductFlashSaleViewSet, 'flash-sale')

urlpatterns = [
    url(r'', include(router.urls)),
]
