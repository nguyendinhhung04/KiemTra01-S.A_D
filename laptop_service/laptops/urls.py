from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaptopViewSet, ManufacturerViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'laptops', LaptopViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
