from django.db import models
from django.contrib.auth.models import User
from item.models import Item


# Create your models here.
class Checkout(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100, blank=True)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    credit_card_number = models.BigIntegerField()
    expiration_month = models.BigIntegerField()
    expiration_year = models.BigIntegerField()
    cvv = models.BigIntegerField()

    def __str__(self):
        return "ID:{} | Buyer:{} ".format(self.pk, self.name)


# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
# User Review
class UserReview(models.Model):
    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=(
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ))

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return "ID:{} | Checkout ID: {}".format(self.pk, self.checkout_id)
