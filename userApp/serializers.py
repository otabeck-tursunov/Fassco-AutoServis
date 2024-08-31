from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'branch', 'role', 'position',
                  'is_superuser', 'date_joined')

        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'max_length': 10},
            'branch': {'read_only': True},
        }


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'branch', 'role', 'position',
                  'is_superuser', 'date_joined')

        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'max_length': 10},
            'branch': {'read_only': True},
        }


class StaffPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'position')

        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'max_length': 10},
        }

    def create(self, validated_data):
        staff = User.objects.create_user(**validated_data)
        return staff


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'branch', 'role', 'position',
            'part', 'balance', 'is_superuser', 'date_joined'
        )

        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'max_length': 10},
            'branch': {'read_only': True},
        }


class ManagerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'position', 'part', 'balance'
        )

        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'max_length': 10},
        }

    def create(self, validated_data):
        manager = User.objects.create_user(**validated_data)
        return manager


class WorkerSerializer(ManagerSerializer):
    def create(self, validated_data):
        worker = User(**validated_data)
        worker.save(role='Worker')
        return worker


class WorkerPostSerializer(ManagerPostSerializer):
    pass

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'branch', 'position', 'role',
#             'is_staff', 'is_superuser', 'last_login', 'date_joined'
#         )
#
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'last_login': {'read_only': True},
#             'date_joined': {'read_only': True},
#             'is_superuser': {'read_only': True},
#             'is_staff': {'read_only': True},
#         }
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         user.is_staff = True
#         user.save()
#         return user
#
#
# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'id', 'username', 'first_name', 'last_name', 'phone_number', 'branch', 'position', 'role', 'salary', 'part',
#             'is_staff', 'is_superuser', 'last_login', 'date_joined'
#         )
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'last_login': {'read_only': True},
#             'date_joined': {'read_only': True},
#             'is_superuser': {'read_only': True},
#             'is_staff': {'read_only': True},
#         }
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         user.is_staff = True
#         user.save()
#         return user
