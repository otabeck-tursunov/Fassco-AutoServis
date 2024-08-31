from django.contrib import admin
from .models import *


class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'branch')
    list_display_links = ('name',)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'description', 'price', 'created_at', 'user', 'branch')
    list_display_links = ('type', 'description')


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 1


class OrderServiceInline(admin.StackedInline):
    model = OrderService
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'paid', 'debt', 'created_at', 'branch')
    list_display_links = ('id', 'customer')
    inlines = [OrderProductInline, OrderServiceInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'total', 'amount', 'discount', 'order', 'branch', 'created_at')
    list_display_links = ('id', 'product')


class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'total', 'part', 'order', 'worker', 'branch', 'created_at')
    list_display_links = ('id', 'service')


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'amount', 'branch', 'created_at', 'description')
    list_display_links = ('id', 'employee')


admin.site.register(ExpenseType, ExpenseTypeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(OrderService, OrderServiceAdmin)
admin.site.register(Salary, SalaryAdmin)
