from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from mainApp.models import *


class User(AbstractUser):
    ROLE_CHOICES = (
        ('SuperStatus', 'SuperStatus'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
        ('Worker', 'Worker'),
    )
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Staff')

    # For Staff, Manager, Worker
    part = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    balance = models.FloatField(default=0)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username