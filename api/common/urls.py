from django.conf.urls import url, include

urlpatterns = [
    url(r'^authentication/', include('api.authentication.urls',)),
    url(r'^product/', include('api.product.urls',)),
]
