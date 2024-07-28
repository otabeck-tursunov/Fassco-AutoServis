from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'branch', 'position',
            'is_staff', 'is_superuser', 'last_login', 'date_joined'
        )

        extra_kwargs = {
            'password': {'<PASSWORD>': True, 'write_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        return user
