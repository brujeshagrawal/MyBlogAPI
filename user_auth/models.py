from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Create your models here.
class User(AbstractUser):

    def __str__(self):
        return "{}".format(self.username)