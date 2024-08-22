from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone number'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branchs')

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone number'))
    phone_number_extra = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone number'))
    passport_serial_numbers = models.CharField(max_length=2, blank=True, null=True,
                                               verbose_name=_('Passport serial numbers'))
    passport_serial_letters = models.CharField(max_length=7, blank=True, null=True,
                                               verbose_name=_('Passport serial letters'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    debt = models.FloatField(default=0, verbose_name=_('Debt'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return self.first_name + " " + self.last_name

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Code'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    brand = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Brand'))
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Color'))
    state_number = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('State number'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self):
        return self.customer.first_name + ": " + self.name


class Provider(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone number'))
    debt = models.FloatField(default=0, verbose_name=_('Debt'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Code'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    amount = models.FloatField(default=0, verbose_name=_('Amount'))
    min_amount = models.FloatField(default=10, verbose_name=_('Minimum amount'))
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Unit'))
    import_price = models.FloatField(verbose_name=_('Import price'))
    export_price = models.FloatField(blank=True, null=True, verbose_name=_('Export price'))
    max_discount = models.FloatField(default=0, verbose_name=_('Max discount'))

    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Provider'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name


class ImportProduct(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))
    amount = models.FloatField(default=0, verbose_name=_('Amount'))
    import_price = models.FloatField(blank=True, null=True, verbose_name=_('Import price'))
    total = models.FloatField(default=0, verbose_name=_('Total'))
    debt = models.FloatField(default=0, verbose_name=_('Debt'))

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Product'))
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Provider'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Import product')
        verbose_name_plural = _('Import products')

    def __str__(self):
        return f"{self.product} {self.amount}"


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    price = models.FloatField(verbose_name=_('Price'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name


# class IProvider(models.Model):
#     provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Provider'))
#     total = models.FloatField(default=0, verbose_name=_('Total'))
#     debt = models.FloatField(default=0, verbose_name=_('Debt'))
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
#
#     class Meta:
#         verbose_name = _('Import from provider')
#         verbose_name_plural = _('Import from providers')
#
#     def __str__(self):
#         return f"{self.provider} {self.total}"
#
#
# class IProduct(models.Model):
#     iProvider = models.ForeignKey(IProvider, on_delete=models.CASCADE, verbose_name=_('Provider'))
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
#     amount = models.FloatField(default=0, verbose_name=_('Amount'))
#
#     def __str__(self):
#         return f"{self.product} {self.amount}"
