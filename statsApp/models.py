from datetime import timezone
from wsgiref.validate import validator

from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator
from django.db import models
from mainApp.models import *
from userApp.models import User


class ExpenseType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Expense Type')
        verbose_name_plural = _('Expense Types')

    def __str__(self):
        return self.name


class Expense(models.Model):
    description = models.TextField(blank=True, verbose_name=_('Description'))
    price = models.FloatField(verbose_name=_('Price'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Type'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('User'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return f"{self.description}"



class Order(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    total = models.FloatField(default=0, verbose_name=_('Total'))
    paid = models.FloatField(default=0, verbose_name=_('Paid'))
    debt = models.FloatField(default=0, verbose_name=_('Debt'))

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('Created at'))

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Customer'))
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Car'))
    car_kilometers = models.FloatField(blank=True, null=True, verbose_name=_('Kilometers'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Manager'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return str(self.customer) + ": " + str(self.total)


class OrderProduct(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    amount = models.FloatField(default=1, verbose_name=_('Amount'))
    discount = models.FloatField(default=0, verbose_name=_('Discount'))
    total = models.FloatField(default=0, verbose_name=_('Total'))

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Product'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Order Product')
        verbose_name_plural = _('Order Products')

    def __str__(self):
        return str(self.order) + ": " + str(self.product)


class OrderService(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    part = models.FloatField(default=1, verbose_name=_('Part'))
    total = models.FloatField(default=0, verbose_name=_('Total'))

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Order'))
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Service'))
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Staff'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Order Service')
        verbose_name_plural = _('Order Services')

    def __str__(self):
        return str(self.order) + ": " + str(self.service)
