from rest_framework import serializers
from .models import *


class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }

    def to_representation(self, instance):
        order = super(OrderSerializer, self).to_representation(instance)

        order_products = OrderProduct.objects.filter(order=instance)
        order_products_serializer = OrderProductSerializer(order_products, many=True)

        order_services = OrderService.objects.filter(order=instance)
        order_services_serializer = OrderServiceSerializer(order_services, many=True)

        order.update(
            {
                'products': order_products_serializer.data,
                'services': order_services_serializer.data
            }
        )
        return order


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderService
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }
