from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Staff
from .serializers import StaffSerializer

def login_view(request):
    return render(request, 'login.html')

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            staff = Staff.objects.get(username=username, password=password)
            serializer = self.get_serializer(staff)
            return Response({
                'message': 'Login successful',
                'staff': serializer.data
            }, status=status.HTTP_200_OK)
        except Staff.DoesNotExist:
            return Response({'error': 'Invalid credentials.'},
                            status=status.HTTP_401_UNAUTHORIZED)
