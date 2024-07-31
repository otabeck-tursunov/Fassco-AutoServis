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
                 'is_superuser',
                 'last_login',
                 'date_joined',
             )
         }
         ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
