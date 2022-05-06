from django.db import models
from django.utils import timezone
from user.models import User


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_type = models.ForeignKey(ItemSalesType, on_delete=models.CASCADE)
    price_minimum = models.FloatField(default=0)
    price_fixed = models.FloatField(null=True, blank=True)
    condition = models.ForeignKey(ItemCondition, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    show_in_catalog = models.BooleanField(default=True)
    date_ends = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    hitcount = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['show_in_catalog', '-hitcount', 'name'], name="item_main_view_index"),
        ]

    def __str__(self):
        res = self.name
        if not self.show_in_catalog:
            res += ' (unlisted)'
        return res

    def current_price(self):
        if self.offer_set.count() > 0:
            highest = self.offer_set.order_by('-amount').first().amount
            if highest > self.price_minimum:
                return highest
        return self.price_minimum

    def number_of_offers(self):
        return self.offer_set.count()


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    url = models.CharField(max_length=10000)
    description = models.CharField(max_length=10000, blank=True)


class Offer(models.Model):
    offer_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.offer_by.first_name + ' wants ' + self.item.name + ' for ' + f'{self.amount:.0f}'

    def __int__(self):
        return round(self.amount)
