from django.conf.urls import url, include
from rest_framework import routers

from .views.cart import CartViewSet
from .views.checkout import CheckOutViewSet
from .views.invoice import InvoiceViewSet

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet, 'cart')
router.register(r'checkout', CheckOutViewSet, 'checkout')
router.register(r'invoice', InvoiceViewSet, 'invoice')

urlpatterns = [
    url('', include(router.urls))
]
