from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import *


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone_number', 'created_at')
    list_display_links = ('name',)


class CarInline(admin.StackedInline):
    model = Car
    extra = 1


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'debt', 'branch', 'created_at')
    list_display_links = ('first_name',)
    inlines = [CarInline]


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'brand', 'color', 'state_number', 'branch', 'customer')
    list_display_links = ('code', 'name')


class ImportProductInline(admin.StackedInline):
    model = ImportProduct
    extra = 1


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'debt', 'branch', 'created_at')
    list_display_links = ('name',)
    inlines = [ImportProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'code', 'name', 'amount', 'unit', 'import_price', 'export_price', 'max_discount', 'provider', 'branch',
        'created_at'
    )
    list_display_links = ('code', 'name')
    inlines = [ImportProductInline]


class ImportProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'amount', 'import_price', 'total', 'debt', 'provider', 'branch', 'created_at')
    list_display_links = ('id', 'product')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'branch', 'created_at')
    list_display_links = ('name',)


admin.site.register(Branch, BranchAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ImportProduct, ImportProductAdmin)
admin.site.register(Service, ServiceAdmin)
