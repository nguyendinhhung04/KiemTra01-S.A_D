from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Laptop(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.URLField(max_length=500)
    properties = models.TextField() # properties (string)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.IntegerField(default=0)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='laptops')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='laptops')
    ram = models.CharField(max_length=50)
    cpu = models.CharField(max_length=255) # CPU
    gpu = models.CharField(max_length=255) # GPU
    screen = models.CharField(max_length=255)

    def __str__(self):
        return self.name
