from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Laptop, Manufacturer, Category
from .serializers import LaptopSerializer, ManufacturerSerializer, CategorySerializer
import chatbot


class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not chatbot.is_graph_ready():
            return Response(
                {"error": "Graph data is still being seeded. Try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            reply = chatbot.chat(user_message)
            return Response({"reply": reply}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
