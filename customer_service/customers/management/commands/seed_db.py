from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from customers.models import Customer, Cart, CartItem

class Command(BaseCommand):
    help = 'Seeds the database with initial customer data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")
        
        # Clear existing data
        # CartItem.objects.all().delete()
        # Cart.objects.all().delete()
        # Customer.objects.all().delete()

        customers_data = [
            {
                'name': 'Nguyễn Văn A',
                'phone': '0123456789',
                'email': 'vana@example.com',
                'username': 'vana',
                'password': 'password123'
            },
            {
                'name': 'Trần Thị B',
                'phone': '0987654321',
                'email': 'thib@example.com',
                'username': 'thib',
                'password': 'password456'
            },
            {
                'name': 'Lê Văn C',
                'phone': '0369852147',
                'email': 'vanc@example.com',
                'username': 'vanc',
                'password': 'password789'
            },
        ]

        try:
            with transaction.atomic():
                for c_data in customers_data:
                    # Create or update Customer
                    customer, created = Customer.objects.update_or_create(
                        username=c_data['username'],
                        defaults={
                            'name': c_data['name'],
                            'phone': c_data['phone'],
                            'email': c_data['email'],
                            'password': c_data['password']
                        }
                    )
                    
                    if created:
                        self.stdout.write(f"Created customer: {customer.username}")
                    else:
                        self.stdout.write(f"Updated customer: {customer.username}")

                    # Ensure each customer has their own unique cart
                    cart, cart_created = Cart.objects.get_or_create(customer=customer)
                    if cart_created:
                        self.stdout.write(f"Created new cart for: {customer.username}")
                    else:
                        self.stdout.write(f"Using existing cart for: {customer.username}")

                    # Add some sample cart items to the cart if it was just created or if it's empty
                    if cart_created or cart.items.count() == 0:
                        CartItem.objects.create(
                            cart=cart,
                            item_id=1,
                            quantity=1,
                            product_type='MOBILE'
                        )
                        CartItem.objects.create(
                            cart=cart,
                            item_id=1, # Sample laptop ID 1
                            quantity=2,
                            product_type='LAPTOP'
                        )
                        self.stdout.write(f"Added sample items to {customer.username}'s cart")

            self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Seeding failed: {str(e)}'))
