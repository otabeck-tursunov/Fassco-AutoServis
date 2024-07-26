from django.contrib import admin
from .models import *

admin.site.register(ExpenseType)
admin.site.register(Expense)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(OrderService)
