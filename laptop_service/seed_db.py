import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_service.settings')
django.setup()

from laptops.models import Manufacturer, Category, Laptop

def seed():
    # Manufacturers
    manufacturers = ['Apple', 'Dell', 'HP', 'Asus', 'Lenovo', 'MSI', 'Acer']
    m_objects = {}
    for name in manufacturers:
        m, created = Manufacturer.objects.get_or_create(name=name)
        m_objects[name] = m
        if created:
            print(f"Created manufacturer: {name}")

    # Categories
    categories = ['Gaming', 'Ultrabook', 'Workstation', 'Student', 'Business']
    c_objects = {}
    for name in categories:
        c, created = Category.objects.get_or_create(name=name)
        c_objects[name] = c
        if created:
            print(f"Created category: {name}")

    # Laptops
    laptops_data = [
        {
            'name': 'MacBook Air M2',
            'img_url': 'https://example.com/macbook-air-m2.jpg',
            'properties': '8-core CPU, 8-core GPU, 8GB Unified Memory, 256GB SSD Storage',
            'price': 1099.00,
            'discount': 5,
            'manufacturer': m_objects['Apple'],
            'category': c_objects['Ultrabook'],
            'ram': '8GB',
            'cpu': 'Apple M2',
            'gpu': '8-core GPU',
            'screen': '13.6-inch Liquid Retina display'
        },
        {
            'name': 'Dell XPS 15',
            'img_url': 'https://example.com/dell-xps-15.jpg',
            'properties': 'Intel Core i7-12700H, 16GB DDR5 RAM, 512GB SSD, RTX 3050 Ti',
            'price': 1899.00,
            'discount': 10,
            'manufacturer': m_objects['Dell'],
            'category': c_objects['Ultrabook'],
            'ram': '16GB',
            'cpu': 'Intel Core i7-12700H',
            'gpu': 'NVIDIA GeForce RTX 3050 Ti',
            'screen': '15.6-inch FHD+'
        },
        {
            'name': 'ASUS ROG Zephyrus G14',
            'img_url': 'https://example.com/rog-zephyrus-g14.jpg',
            'properties': 'Ryzen 9 6900HS, 16GB DDR5, 1TB SSD, Radeon RX 6700S',
            'price': 1649.00,
            'discount': 0,
            'manufacturer': m_objects['Asus'],
            'category': c_objects['Gaming'],
            'ram': '16GB',
            'cpu': 'AMD Ryzen 9 6900HS',
            'gpu': 'AMD Radeon RX 6700S',
            'screen': '14-inch QHD 120Hz'
        },
        {
            'name': 'HP Pavilion 15',
            'img_url': 'https://example.com/hp-pavilion-15.jpg',
            'properties': 'Intel Core i5-1235U, 8GB RAM, 256GB SSD',
            'price': 599.00,
            'discount': 15,
            'manufacturer': m_objects['HP'],
            'category': c_objects['Student'],
            'ram': '8GB',
            'cpu': 'Intel Core i5-1235U',
            'gpu': 'Intel Iris Xe Graphics',
            'screen': '15.6-inch FHD'
        },
        {
            'name': 'Lenovo ThinkPad X1 Carbon',
            'img_url': 'https://example.com/thinkpad-x1.jpg',
            'properties': 'Intel Core i7-1260P, 16GB RAM, 512GB SSD',
            'price': 1549.00,
            'discount': 8,
            'manufacturer': m_objects['Lenovo'],
            'category': c_objects['Business'],
            'ram': '16GB',
            'cpu': 'Intel Core i7-1260P',
            'gpu': 'Intel Iris Xe Graphics',
            'screen': '14-inch WUXGA'
        }
    ]

    for data in laptops_data:
        laptop, created = Laptop.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"Created laptop: {data['name']}")
        else:
            print(f"Laptop already exists: {data['name']}")

if __name__ == '__main__':
    print("Seeding database...")
    seed()
    print("Seeding completed.")
