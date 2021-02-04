from django.conf.urls import url, include
from rest_framework import routers
from .views import RegisterViewSet, LoginViewSet

router = routers.DefaultRouter()
router.register(r'register', RegisterViewSet, 'register')
router.register(r'login', LoginViewSet, 'login')

urlpatterns = [
    url(r'', include(router.urls)),
]
