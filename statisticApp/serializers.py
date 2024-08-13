from rest_framework import serializers

from mainApp.models import Customer
from mainApp.serializers import ProductSerializer, CustomerSerializer


class ProductSalesSerializer(serializers.Serializer):
    product = ProductSerializer()
    total_sales = serializers.FloatField(min_value=0)


class TopCustomersSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    customer_full_name = serializers.CharField()
    total_paid = serializers.FloatField(min_value=0)
    orders_count = serializers.IntegerField(min_value=0)


class MonthlyTotalSerializer(serializers.Serializer):
    jan = serializers.FloatField()
    feb = serializers.FloatField()
    mar = serializers.FloatField()
    apr = serializers.FloatField()
    may = serializers.FloatField()
    jun = serializers.FloatField()
    jul = serializers.FloatField()
    aug = serializers.FloatField()
    sep = serializers.FloatField()
    oct = serializers.FloatField()
    nov = serializers.FloatField()
    dec = serializers.FloatField()
