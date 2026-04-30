from django.urls import path
from .views import ChatView, StatusView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='ai_chat'),
    path('status/', StatusView.as_view(), name='ai_status'),
]
