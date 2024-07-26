from django.db import models
from django.contrib.auth.models import AbstractUser

from mainApp.models import *


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    )
    phone_number = models.CharField(max_length=13)
    role = models.CharField(max_length=20)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
