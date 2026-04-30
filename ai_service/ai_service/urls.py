from django.urls import path, include

urlpatterns = [
    path('ai/', include('ai_chatbot.urls')),
]
