from rest_framework import viewsets, status, response, views
from .models import Customer, Cart, CartItem
from .serializers import CustomerSerializer, CartSerializer, CartItemSerializer, RegisterSerializer, LoginSerializer
from django.shortcuts import render

class RegisterView(views.APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return response.Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                customer = Customer.objects.get(username=username, password=password)
                return response.Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return response.Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# UI Views
def login_ui(request):
    return render(request, 'login.html')

def register_ui(request):
    return render(request, 'register.html')

def home_ui(request):
    return render(request, 'home.html')

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
