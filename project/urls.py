from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include

# swagger
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    url(r'^api/', include('api.common.urls'))
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Test Evermos Store",
            default_version='v1',
            description="Assessment Evermos BE",
            contact=openapi.Contact(email="fizikurniawan@gmail.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        url=settings.BASE_URL,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns.append(url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'))
    urlpatterns.append(url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
    urlpatterns.append(url(r'^redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'))