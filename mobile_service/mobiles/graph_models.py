from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom

class Manufacturer(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    # Relationship to mobiles
    mobiles = RelationshipFrom('Mobile', 'MADE_BY')

class Category(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    # Relationship to mobiles
    mobiles = RelationshipFrom('Mobile', 'BELONGS_TO')

class CPU(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    # Relationship to mobiles
    mobiles = RelationshipFrom('Mobile', 'HAS_CPU')

class GPU(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    # Relationship to mobiles
    mobiles = RelationshipFrom('Mobile', 'HAS_GPU')

class RAM(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    # Relationship to mobiles
    mobiles = RelationshipFrom('Mobile', 'HAS_RAM')

class Camera(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    # Relationship to mobiles
    mobiles = RelationshipFrom('Mobile', 'HAS_CAMERA')

class Mobile(StructuredNode):
    product_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)
    price = FloatProperty()
    discount = IntegerProperty(default=0)
    description = StringProperty()

    # Relationships
    manufacturer = RelationshipTo(Manufacturer, 'MADE_BY')
    category = RelationshipTo(Category, 'BELONGS_TO')
    cpu = RelationshipTo(CPU, 'HAS_CPU')
    gpu = RelationshipTo(GPU, 'HAS_GPU')
    ram = RelationshipTo(RAM, 'HAS_RAM')
    camera = RelationshipTo(Camera, 'HAS_CAMERA')