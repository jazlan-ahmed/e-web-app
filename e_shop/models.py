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