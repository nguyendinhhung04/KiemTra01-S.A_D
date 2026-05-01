from rest_framework import viewsets, status, response, views
from rest_framework.decorators import action
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

def cart_ui(request):
    return render(request, 'cart.html')

def product_detail_ui(request, product_type, product_id):
    return render(request, 'product_detail.html', {
        'product_type': product_type,
        'product_id': product_id
    })

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        return response.Response({'message': 'Order placed successfully'}, status=status.HTTP_200_OK)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        item_id = request.data.get('item_id')
        product_type = request.data.get('product_type')
        quantity = int(request.data.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart_id,
            item_id=item_id,
            product_type=product_type,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
