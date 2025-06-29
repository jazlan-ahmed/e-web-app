from django.db import models

# Create your models here.
    
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