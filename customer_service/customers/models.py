from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.customer.username}"

class CartItem(models.Model):
    PRODUCT_TYPES = (
        ('MOBILE', 'MOBILE'),
        ('LAPTOP', 'LAPTOP'),
    )
    item_id = models.IntegerField() # ID of product from laptop_service or mobile_service
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)

    def __str__(self):
        return f"{self.product_type} - Item ID: {self.item_id}"
