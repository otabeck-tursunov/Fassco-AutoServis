from django.db import models
from django.contrib.auth.models import AbstractUser

from mainApp.models import *


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    )

    phone_number = models.CharField(max_length=13, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Staff')

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username
