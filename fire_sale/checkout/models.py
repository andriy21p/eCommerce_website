from django.db import models
from django.contrib.auth.models import User
from ..item.models import Item
from django_countries.fields import CountryField


# Create your models here.

class Checkout(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100, blank=True)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
