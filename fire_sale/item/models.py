from django.db import models
from django.utils import timezone


# Create your models here.
class ItemSalesType(models.Model):
    name = models.CharField(max_length=200)
    buyItNow = models.BooleanField(default=False)
    auction = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ItemCondition(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    sale_type = models.ForeignKey(ItemSalesType, on_delete=models.CASCADE)
    price_minimum = models.FloatField(default=0)
    price_fixed = models.FloatField(null=True, blank=True)
    condition = models.ForeignKey(ItemCondition, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    show_in_catalog = models.BooleanField(default=False)
    date_ends = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)

    def __str__(self):
        res = self.name
        if not self.show_in_catalog:
            res += ' (unlisted)'
        return res


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    url = models.CharField(max_length=10000)
    description = models.CharField(max_length=10000, blank=True)
