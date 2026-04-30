from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom

# Common Models
class Manufacturer(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class Category(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class CPU(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class GPU(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class RAM(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

# Laptop Specific
class Screen(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class Laptop(StructuredNode):
    product_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    price = FloatProperty()
    discount = IntegerProperty(default=0)
    description = StringProperty()

    manufacturer = RelationshipTo(Manufacturer, 'MADE_BY')
    category = RelationshipTo(Category, 'BELONGS_TO')
    cpu = RelationshipTo(CPU, 'HAS_CPU')
    gpu = RelationshipTo(GPU, 'HAS_GPU')
    ram = RelationshipTo(RAM, 'HAS_RAM')
    screen = RelationshipTo(Screen, 'HAS_SCREEN')

# Mobile Specific
class Camera(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class Mobile(StructuredNode):
    product_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    price = FloatProperty()
    discount = IntegerProperty(default=0)
    description = StringProperty()

    manufacturer = RelationshipTo(Manufacturer, 'MADE_BY')
    category = RelationshipTo(Category, 'BELONGS_TO')
    cpu = RelationshipTo(CPU, 'HAS_CPU')
    gpu = RelationshipTo(GPU, 'HAS_GPU')
    ram = RelationshipTo(RAM, 'HAS_RAM')
    camera = RelationshipTo(Camera, 'HAS_CAMERA')
