from django.utils.translation import gettext_lazy as _
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
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone Number'))
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Position'))
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Staff', verbose_name=_('Role'))

    # For Staff, Manager, Worker
    part = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=1, verbose_name=_('Part'))
    balance = models.FloatField(default=0, blank=True, null=True, verbose_name=_('Balance'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Branch'))

    def __str__(self):
        return self.username