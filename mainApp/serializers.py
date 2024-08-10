from django.db.models import Sum
from rest_framework import serializers

from statsApp.models import OrderProduct
from .models import *


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class CarSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Car
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class CarPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()

    class Meta:
        model = Product
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }

    def to_representation(self, instance):
        product = super(ProductSerializer, self).to_representation(instance)

        total_export = OrderProduct.objects.filter(product=instance).aggregate(total_sum=Sum('total'))['total_sum'] or 0
        product['total_export'] = total_export

        total_import = ImportProduct.objects.filter(product=instance).aggregate(total_import=Sum('total'))[
                           'total_import'] or 0
        product['total_import'] = total_import

        total_benefit = total_export - total_import
        product['total_benefit'] = total_benefit

        return product


class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class ImportProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ImportProduct
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class ImportProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportProduct
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True}
        }
