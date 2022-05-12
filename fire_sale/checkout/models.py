from django.db import models
from django.contrib.auth.models import User
from item.models import Offer
from datetime import date


# Create your models here.

def get_year_choice():
    year_list = [year for year in range(date.today().year, date.today().year+9)]
    choice = tuple(enumerate(year_list, 1))
    return choice


class Country(models.Model):
    countryId = models.CharField(max_length=10)
    countryName = models.CharField(max_length=500)
    countryNameIs = models.CharField(max_length=500)

    def __str__(self):
        return self.countryId + ': ' + self.countryName


class Checkout(models.Model):
    # Create choices for credit card information
    MONTH_CHOICE = ((1, "Jan"),
                    (2, "Feb"),
                    (3, "Mar"),
                    (4, "Apr"),
                    (5, "May"),
                    (6, "Jun"),
                    (7, "Jul"),
                    (8, "Aug"),
                    (9, "Sep"),
                    (10, "Oct"),
                    (11, "Nov"),
                    (12, "Dec")
                    )

    YEAR_CHOICE = get_year_choice()

    offer = models.OneToOneField(Offer, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, default=243, null=True, blank=True);
    postal_code = models.CharField(max_length=100, blank=True)
    credit_card_holder = models.CharField(max_length=100, blank=True)
    credit_card_number = models.PositiveBigIntegerField()
    expiration_month = models.IntegerField(choices=MONTH_CHOICE)
    expiration_year = models.IntegerField(choices=YEAR_CHOICE)
    cvv = models.PositiveSmallIntegerField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "ID:{} | Order ID:{} ".format(self.pk, self.offer)


# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
# User Review
class UserReview(models.Model):
    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=10000)
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
        return "ID:{} | Checkout ID: {}".format(self.pk, self.checkout.id)



