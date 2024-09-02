from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Auth",
         {
             'fields':
                 (
                     'username',
                     'password'
                 )
         }
         ),
        ('Personal info',
         {'fields':
             (
                 'first_name',
                 'last_name',
                 'phone_number',
                 'branch',
                 'role',
                 'position',
                 'part',
                 'balance',
                 'is_superuser',
                 'is_staff',
                 'last_login',
                 'date_joined',
             )
         }
         ),
    )

    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'branch', 'role', 'position', 'is_staff')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'branch', 'role', 'position')



admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
