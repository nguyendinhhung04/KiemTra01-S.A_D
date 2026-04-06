"""
URL configuration for customer_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from customers.views import home_ui, login_ui, register_ui, cart_ui

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('customers.urls')),
    path('home/', home_ui, name='home'),
    path('login/', login_ui, name='login-ui'),
    path('register/', register_ui, name='register-ui'),
    path('ui/cart/', cart_ui, name='cart-ui'),
]
