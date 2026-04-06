from django.core.management.base import BaseCommand
from mobiles.models import Manufacturer, Category, Mobile
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial mobile data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create Manufacturers
        manufacturers_data = ['Apple', 'Samsung', 'Xiaomi', 'Oppo', 'Vivo', 'Sony']
        manufacturers = []
        for name in manufacturers_data:
            m, created = Manufacturer.objects.get_or_create(name=name)
            manufacturers.append(m)
            if created:
                self.stdout.write(f'Created Manufacturer: {name}')

        # Create Categories
        categories_data = ['Smartphone', 'Gaming Phone', 'Foldable', 'Budget Phone']
        categories = []
        for name in categories_data:
            c, created = Category.objects.get_or_create(name=name)
            categories.append(c)
            if created:
                self.stdout.write(f'Created Category: {name}')

        # Create Mobiles
        mobiles_data = [
            {
                'name': 'iPhone 15 Pro Max',
                'img_url': 'https://example.com/iphone15.jpg',
                'price': 1199.99,
                'discount': 5,
                'manufacturer': 'Apple',
                'category': 'Smartphone',
                'ram': '8GB',
                'cpu': 'A17 Pro',
                'gpu': 'Apple GPU (6-core)',
                'camera': '48MP Main, 12MP Ultra Wide, 12MP Telephoto'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'img_url': 'https://example.com/s24ultra.jpg',
                'price': 1299.99,
                'discount': 10,
                'manufacturer': 'Samsung',
                'category': 'Smartphone',
                'ram': '12GB',
                'cpu': 'Snapdragon 8 Gen 3',
                'gpu': 'Adreno 750',
                'camera': '200MP Main, 12MP Ultra Wide, 10MP Telephoto, 50MP Periscope'
            },
            {
                'name': 'Xiaomi 14 Ultra',
                'img_url': 'https://example.com/xiaomi14.jpg',
                'price': 999.00,
                'discount': 15,
                'manufacturer': 'Xiaomi',
                'category': 'Smartphone',
                'ram': '16GB',
                'cpu': 'Snapdragon 8 Gen 3',
                'gpu': 'Adreno 750',
                'camera': '50MP Quad Camera System'
            },
            {
                'name': 'ASUS ROG Phone 8',
                'img_url': 'https://example.com/rog8.jpg',
                'price': 1099.00,
                'discount': 0,
                'manufacturer': 'Sony', # Sony used as placeholder for ROG in this simple list
                'category': 'Gaming Phone',
                'ram': '16GB',
                'cpu': 'Snapdragon 8 Gen 3',
                'gpu': 'Adreno 750',
                'camera': '50MP Main, 13MP Ultra Wide, 32MP Telephoto'
            },
            {
                'name': 'Samsung Galaxy Z Fold 5',
                'img_url': 'https://example.com/zfold5.jpg',
                'price': 1799.99,
                'discount': 20,
                'manufacturer': 'Samsung',
                'category': 'Foldable',
                'ram': '12GB',
                'cpu': 'Snapdragon 8 Gen 2',
                'gpu': 'Adreno 740',
                'camera': '50MP Main, 12MP Ultra Wide, 10MP Telephoto'
            }
        ]

        for mobile in mobiles_data:
            manufacturer = Manufacturer.objects.get(name=mobile['manufacturer'])
            category = Category.objects.get(name=mobile['category'])
            
            m, created = Mobile.objects.get_or_create(
                name=mobile['name'],
                defaults={
                    'img_url': mobile['img_url'],
                    'price': mobile['price'],
                    'discount': mobile['discount'],
                    'manufacturer': manufacturer,
                    'category': category,
                    'ram': mobile['ram'],
                    'cpu': mobile['cpu'],
                    'gpu': mobile['gpu'],
                    'camera': mobile['camera'],
                }
            )
            if created:
                self.stdout.write(f'Created Mobile: {mobile["name"]}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
