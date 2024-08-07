from rest_framework import serializers

from mainApp.serializers import ProductSerializer


class ProductSalesSerializer(serializers.Serializer):
    product = ProductSerializer()
    total_sales = serializers.FloatField()
