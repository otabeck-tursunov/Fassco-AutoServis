import json

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from mainApp.models import Product
from statsApp.models import OrderProduct
from statsApp.serializers import OrderProductSerializer
from .serializers import *


class TopSaleProductAPIView(APIView):
    def get(self, request):
        top_products = OrderProduct.objects.values('product').annotate(total_sales=Sum('total')).order_by(
            '-total_sales')[:3]

        data = []
        for product in top_products:
            _product = get_object_or_404(Product, id=product['product'])
            total_sales = product['total_sales']
            data.append(
                {
                    'product': _product,
                    'total_sales': total_sales
                }
            )
        serializer = ProductSalesSerializer(data, many=True)
        return Response(serializer.data)
