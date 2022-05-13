from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=1000, blank=True)
    bio = models.CharField(max_length=10000, blank=True)

    def __str__(self):
        return self.user.first_name

    @property
    def number_of_unread_message(self):
        number = self.user.msg_receiver.filter(receiver=self.user_id, msg_received__isnull=True).count()
        return number

    def avg_rating(self):
        """ Uses AVG rating based on User Review per seller."""
        avg_rating_return = self.user.userreview_set.aggregate(Avg('rating'))
        return avg_rating_return

    @property
    def avg_rating_percent(self):
        """ Uses AVG rating based on User Review per seller."""
        avg_rating_return = self.user.userreview_set.aggregate(Avg('rating'))
        if avg_rating_return['rating__avg'] is None:
            perc = 90
        else:
            perc = round(avg_rating_return['rating__avg'] * 2) * 10
        return perc


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



