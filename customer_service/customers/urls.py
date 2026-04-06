from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, CartViewSet, CartItemViewSet, 
    RegisterView, LoginView, 
    login_ui, register_ui, home_ui
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # UI Routes
    path('ui/login/', login_ui, name='login-ui'),
    path('ui/register/', register_ui, name='register-ui'),
]
