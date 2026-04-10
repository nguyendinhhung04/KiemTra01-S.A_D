from django.urls import path, re_path
from .views import proxy_view

urlpatterns = [
    re_path(r'^(?P<service_name>[^/]+)/(?P<path>.*)$', proxy_view, name='proxy'),
]
