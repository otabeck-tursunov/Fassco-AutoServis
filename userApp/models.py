from django.db import models
from django.contrib.auth.models import AbstractUser

from mainApp.models import *


class User(AbstractUser):
    phone_number = models.CharField(max_length=13)
    position = models.CharField(max_length=50, blank=True, null=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
