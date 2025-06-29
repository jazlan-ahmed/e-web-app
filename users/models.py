from django.db import models

# Create your models here.

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