from django.db import models
from mainApp.models import *
from userApp.models import User


class ExpenseType(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(models.Model):
    description = models.TextField(blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.type.name + " " + self.price


class Order(models.Model):
    total = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    debt = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer) + ": " + str(self.total)


class OrderProduct(models.Model):
    amount = models.FloatField(default=1)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.order) + ": " + str(self.product)


class OrderService(models.Model):
    part = models.FloatField(default=1)
    total = models.FloatField(default=0)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.order) + ": " + str(self.service)



