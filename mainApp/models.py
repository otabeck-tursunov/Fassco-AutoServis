from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    phone_number_extra = models.CharField(max_length=13, blank=True, null=True)
    passport_serial_numbers = models.CharField(max_length=2, blank=True, null=True)
    passport_serial_letters = models.CharField(max_length=7, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    debt = models.FloatField(default=0)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Car(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    state_number = models.CharField(max_length=10, blank=True, null=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.first_name + ": " + self.name


class Provider(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    debt = models.FloatField(default=0)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=255)
    amount = models.FloatField(default=0)
    unit = models.CharField(max_length=50, blank=True, null=True)
    import_price = models.FloatField()
    export_price = models.FloatField(blank=True, null=True)
    max_discount = models.FloatField(default=0)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ImportProduct(models.Model):
    amount = models.FloatField(default=0)
    debt = models.FloatField(default=0)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
