from rest_framework import serializers

from mainApp.serializers import CustomerSerializer, ProductSerializer, ServiceSerializer, CarSerializer
from .models import *


class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class ExpenseSerializer(serializers.ModelSerializer):
    type = ExpenseTypeSerializer()

    class Meta:
        model = Expense
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class ExpensePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    car = CarSerializer()

    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }

    def to_representation(self, instance):
        order = super(OrderSerializer, self).to_representation(instance)

        order_products = OrderProduct.objects.filter(order=instance)
        order_products_serializer = OrderProductCascadeSerializer(order_products, many=True)

        order_services = OrderService.objects.filter(order=instance)
        order_services_serializer = OrderServiceCascadeSerializer(order_services, many=True)

        order.update(
            {
                'products': order_products_serializer.data,
                'services': order_services_serializer.data
            }
        )
        return order


class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }

    def to_representation(self, instance):
        order = super(OrderPostSerializer, self).to_representation(instance)

        order_products = OrderProduct.objects.filter(order=instance)
        order_products_serializer = OrderServicePostSerializer(order_products, many=True)

        order_services = OrderService.objects.filter(order=instance)
        order_services_serializer = OrderServicePostSerializer(order_services, many=True)

        order.update(
            {
                'products': order_products_serializer.data,
                'services': order_services_serializer.data
            }
        )
        return order


class OrderProductCascadeSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderProductSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderServiceCascadeSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = OrderService
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderServiceSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    service = ServiceSerializer()

    class Meta:
        model = OrderService
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }


class OrderServicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderService
        fields = '__all__'

        extra_kwargs = {
            'branch': {'read_only': True},
        }
