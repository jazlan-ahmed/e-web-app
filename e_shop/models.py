from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    originalPrice = models.IntegerField()
    offerPrice = models.IntegerField()
    availableOffers = models.TextField()
    highlights = models.TextField()
    seller = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    company = models.TextField(max_length=50)
    
class Cart(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Cart_images')
    originalPrice = models.IntegerField()
    offerPrice = models.IntegerField()
    seller = models.CharField(max_length=50)
    quantity = models.IntegerField()

class Orders(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='orders')
    originalPrice = models.IntegerField()
    offerPrice = models.IntegerField()
    seller = models.CharField(max_length=50)
    quantity = models.IntegerField()
    
class Address(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    address = models.CharField()
    city = models.CharField(max_length=50)
    state = models.CharField()
    landmark = models.CharField()
    alternative_mobile = models.CharField()