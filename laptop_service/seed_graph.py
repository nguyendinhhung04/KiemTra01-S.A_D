import os
import django
import json
import time
from neomodel import config

GRAPH_READY_FILE = "/tmp/laptop_graph_ready"

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_service.settings')
django.setup()

# Configure neomodel
config.DATABASE_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:password@neo4j:7687')

from laptops.graph_models import Laptop, Manufacturer, Category, CPU, GPU, RAM, Screen

def wait_for_neo4j(max_retries=60, delay=5):
    """Wait for Neo4j to be available (Total 5 minutes)"""
    for attempt in range(max_retries):
        try:
            from neomodel import db
            db.cypher_query("RETURN 1")
            print("✓ Connected to Neo4j")
            return True
        except Exception as e:
            print(f"Neo4j not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    print("✗ Failed to connect to Neo4j after retries")
    return False

def seed_graph():
    if os.path.exists(GRAPH_READY_FILE):
        os.remove(GRAPH_READY_FILE)

    # Wait for Neo4j to be available
    if not wait_for_neo4j():
        return
    
    # Load knowledge base
    with open('knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    laptops = data['laptops']

    for laptop_data in laptops:
        # Create or get manufacturer
        manufacturer = Manufacturer.get_or_create({'name': laptop_data['manufacturer']})[0]

        # Create or get category
        category = Category.get_or_create({'name': laptop_data['category']})[0]

        # Create or get CPU
        cpu = CPU.get_or_create({'name': laptop_data['specs']['cpu']})[0]

        # Create or get GPU
        gpu = GPU.get_or_create({'name': laptop_data['specs']['gpu']})[0]

        # Create or get RAM
        ram = RAM.get_or_create({'name': laptop_data['specs']['ram']})[0]

        # Create or get Screen
        screen = Screen.get_or_create({'name': laptop_data['specs']['screen']})[0]

        # Keep seeding idempotent across container restarts.
        laptop = Laptop.nodes.get_or_none(product_id=laptop_data['id'])
        if laptop is None:
            laptop = Laptop(
                product_id=laptop_data['id'],
                name=laptop_data['name'],
                price=laptop_data['price'],
                discount=laptop_data['discount'],
                description=laptop_data['description']
            ).save()
        else:
            laptop.name = laptop_data['name']
            laptop.price = laptop_data['price']
            laptop.discount = laptop_data['discount']
            laptop.description = laptop_data['description']
            laptop.save()

        # Create relationships
        if not laptop.manufacturer.is_connected(manufacturer):
            laptop.manufacturer.connect(manufacturer)
        if not laptop.category.is_connected(category):
            laptop.category.connect(category)
        if not laptop.cpu.is_connected(cpu):
            laptop.cpu.connect(cpu)
        if not laptop.gpu.is_connected(gpu):
            laptop.gpu.connect(gpu)
        if not laptop.ram.is_connected(ram):
            laptop.ram.connect(ram)
        if not laptop.screen.is_connected(screen):
            laptop.screen.connect(screen)

        print(f"Created laptop: {laptop.name}")

    with open(GRAPH_READY_FILE, 'w', encoding='utf-8') as ready_file:
        ready_file.write('ready')

if __name__ == '__main__':
    seed_graph()
