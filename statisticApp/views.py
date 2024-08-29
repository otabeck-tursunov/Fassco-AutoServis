from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
import calendar

from mainApp.models import *
from statsApp.models import OrderProduct, Order, Expense, ExpenseType
from userApp.permissions import IsStaffStatus
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


class TopCustomersAPIView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        result = []

        for customer in customers:
            orders = Order.objects.filter(customer=customer)
            count = orders.count()
            total_paid = orders.aggregate(total_paid=Sum('total'))['total_paid']

            result.append(
                {
                    'customer_id': customer.id,
                    'customer_full_name': customer.full_name(),
                    'total_paid': total_paid,
                    'orders_count': count
                }
            )
        serializer = TopCustomersSerializer(result, many=True)
        return Response(serializer.data)


class MonthlyTotalsAPIView(APIView):
    def get(self, request):
        # Hozirgi sana va bir yil oldingi sanani olish
        now = timezone.now()
        one_year_ago = now.replace(day=1) - timezone.timedelta(days=365)

        # So'nggi 1 yil davomida OrderProduct obyektlarini oyma-oy guruhlash
        totals = OrderProduct.objects.filter(created_at__gte=one_year_ago) \
            .annotate(month=TruncMonth('created_at')) \
            .values('month') \
            .annotate(total_sum=Sum('total')) \
            .order_by('month')

        # Boshlang'ich oy dictionary, 0.0 bilan to'ldirilgan
        result = {calendar.month_abbr[i].lower(): 0.0 for i in range(1, 13)}

        # Natijalarni to'ldirish
        for total in totals:
            month = total['month'].month
            month_name = calendar.month_abbr[month].lower()
            result[month_name] = total['total_sum']

        # Hozirgi oy indexini olish
        start_month = now.month
        ordered_result = {}

        # Oylarni hozirgi oydan boshlab tartiblash
        months = list(result.keys())
        for i in range(12):
            month_name = calendar.month_abbr[(start_month + i - 1) % 12 + 1].lower()
            ordered_result[month_name] = result[month_name]

        serializer = MonthlyTotalSerializer(ordered_result)
        return Response(serializer.data)


class StatisticsAPIView(APIView):
    permission_classes = (IsStaffStatus,)

    def get(self, request):
        products = Product.objects.filter(branch=request.user.branch)
        serializer = ProductSerializer(products, many=True)
        total_import = 0
        for product in serializer.data:
            total_import += product['total_import']

        total_export = 0
        for product in serializer.data:
            total_export += product['total_export']

        total_benefit = 0
        for product in serializer.data:
            total_benefit += product['total_benefit']

        serializer_result = StatisticSerializer(
            {
                'total_import': total_import,
                'total_export': total_export,
                'total_benefit': total_benefit
            }
        )
        return Response(serializer_result.data)


class ExpensesStatisticsAPIView(APIView):
    permission_classes = [IsStaffStatus]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='start_date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by Start Date',
            ),
            openapi.Parameter(
                name='end_date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by End Date',
            ),
        ]
    )
    def get(self, request):
        expense_types = ExpenseType.objects.filter(branch=request.user.branch)

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        expenses = None
        if start_date is not None or end_date is not None:
            if start_date is not None:
                expenses = Expense.objects.filter(created_at__gte=start_date, branch=request.user.branch)
            if end_date is not None:
                expenses = Expense.objects.filter(created_at__lte=end_date, branch=request.user.branch)
        else:
            expenses = Expense.objects.filter(branch=request.user.branch)

        result = {}
        for expense_type in expense_types:
            total_price = expenses.filter(type=expense_type).aggregate(Sum('price'))['price__sum'] or 0
            result[expense_type.name] = total_price

        return Response(result, status=status.HTTP_200_OK)
