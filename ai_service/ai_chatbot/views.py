from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import chatbot_logic


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            reply = chatbot_logic.chat(user_message)
            return Response({"reply": reply}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatusView(APIView):
    def get(self, request):
        is_ready = chatbot_logic.is_model_ready()
        return Response({
            "status": "ready" if is_ready else "loading",
            "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        }, status=status.HTTP_200_OK)
