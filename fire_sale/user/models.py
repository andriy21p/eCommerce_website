from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=1000)
    bio = models.CharField(max_length=10000)

    def __str__(self):
        return self.name
