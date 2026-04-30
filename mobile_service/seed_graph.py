import os
import django
import json
import time
from neomodel import config

GRAPH_READY_FILE = "/tmp/mobile_graph_ready"

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mobile_service.settings')
django.setup()

# Configure neomodel
config.DATABASE_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:password@neo4j:7687')

from mobiles.graph_models import Mobile, Manufacturer, Category, CPU, GPU, RAM, Camera

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

    mobiles = data['mobiles']

    for mobile_data in mobiles:
        # Create or get manufacturer
        manufacturer = Manufacturer.get_or_create({'name': mobile_data['manufacturer']})[0]

        # Create or get category
        category = Category.get_or_create({'name': mobile_data['category']})[0]

        # Create or get CPU
        cpu = CPU.get_or_create({'name': mobile_data['specs']['cpu']})[0]

        # Create or get GPU
        gpu = GPU.get_or_create({'name': mobile_data['specs']['gpu']})[0]

        # Create or get RAM
        ram = RAM.get_or_create({'name': mobile_data['specs']['ram']})[0]

        # Create or get Camera
        camera = Camera.get_or_create({'name': mobile_data['specs']['camera']})[0]

        # Keep seeding idempotent across container restarts.
        mobile = Mobile.nodes.get_or_none(product_id=mobile_data['id'])
        if mobile is None:
            mobile = Mobile(
                product_id=mobile_data['id'],
                name=mobile_data['name'],
                price=mobile_data['price'],
                discount=mobile_data.get('discount', 0),
                description=mobile_data.get('description', '')
            ).save()
        else:
            mobile.name = mobile_data['name']
            mobile.price = mobile_data['price']
            mobile.discount = mobile_data.get('discount', 0)
            mobile.description = mobile_data.get('description', '')
            mobile.save()

        # Create relationships
        if not mobile.manufacturer.is_connected(manufacturer):
            mobile.manufacturer.connect(manufacturer)
        if not mobile.category.is_connected(category):
            mobile.category.connect(category)
        if not mobile.cpu.is_connected(cpu):
            mobile.cpu.connect(cpu)
        if not mobile.gpu.is_connected(gpu):
            mobile.gpu.connect(gpu)
        if not mobile.ram.is_connected(ram):
            mobile.ram.connect(ram)
        if not mobile.camera.is_connected(camera):
            mobile.camera.connect(camera)

        print(f"Created mobile: {mobile.name}")

    with open(GRAPH_READY_FILE, 'w', encoding='utf-8') as ready_file:
        ready_file.write('ready')

if __name__ == '__main__':
    seed_graph()
