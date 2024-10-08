from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from userApp.permissions import IsStaffStatus
from .serializers import *
from .models import *


class ExpenseTypeListCreateView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = ExpenseType.objects.all().order_by('id')
    serializer_class = ExpenseTypeSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class ExpenseTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer

    def get_object(self):
        return get_object_or_404(ExpenseType, pk=self.kwargs['pk'], branch=self.request.user.branch)


class ExpenseListCreateView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Expense.objects.all().order_by('id')
    serializer_class = ExpenseSerializer

    filter_backends = [SearchFilter, OrderingFilter, ]
    search_fields = ['description'],
    ordering_fields = '__all__'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExpenseSerializer
        return ExpensePostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch, user=self.request.user)


class ExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffStatus, ]

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return ExpenseSerializer
        return ExpensePostSerializer

    def get_object(self):
        return get_object_or_404(Expense, pk=self.kwargs['pk'], branch=self.request.user.branch)


class OrderListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = '__all__'
    search_fields = ['customer__first_name', 'customer__last_name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        return OrderPostSerializer

    def perform_create(self, serializer):
        # Save the order
        order = serializer.save(branch=self.request.user.branch)

        # Update the customer's debt by adding the order's debt
        if order.customer:
            order.customer.debt += order.debt
            order.customer.save()

        if order.manager:
            order.manager.balance += order.total * order.manager.part
            order.manager.save()

        if order.branch:
            order.branch.balance += order.total
            order.branch.save()

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return OrderSerializer
        return OrderPostSerializer

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs['pk'], branch=self.request.user.branch)

    def perform_update(self, serializer):
        # Get the current order instance
        order = self.get_object()

        # Store the previous debt value before updating
        previous_debt = order.debt
        previous_total = order.total

        # Update the order
        updated_order = serializer.save()

        # Update customer's debt based on the change in order debt
        if updated_order.customer:
            debt_difference = updated_order.debt - previous_debt
            updated_order.customer.debt += debt_difference
            updated_order.customer.save()

        if updated_order.manager:
            total_difference = updated_order.total - previous_total
            updated_order.manager.balance += total_difference * updated_order.manager.part
            updated_order.manager.save()

        if updated_order.branch:
            total_difference = updated_order.total - previous_total
            updated_order.branch.balance += total_difference
            updated_order.branch.save()

    def perform_destroy(self, instance):
        instance.delete()

        if instance.manager:
            instance.manager.balance -= instance.total * instance.manager.part
            instance.manager.save()

        if instance.customer:
            instance.customer.debt -= instance.debt

        if instance.branch:
            instance.branch.balance -= instance.total


class OrderProductListCreateAPIView(APIView):
    permission_classes = (IsStaffStatus,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by Order ID',
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request):
        order_products = OrderProduct.objects.filter(branch=self.request.user.branch).order_by('id')

        filter_order_id = request.query_params.get('order_id', None)
        if filter_order_id is not None:
            get_object_or_404(Order, pk=filter_order_id)
            order_products = order_products.filter(order_id=filter_order_id)

        search = request.query_params.get('search', None)
        if search is not None:
            order_products = order_products.filter(
                Q(order__customer__first_name__icontains=search) |
                Q(order__customer__last_name__icontains=search) |
                Q(product__name__icontains=search)

            )

        serializer = OrderProductSerializer(order_products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=OrderProductPostSerializer,
    )
    def post(self, request):
        serializer = OrderProductPostSerializer(data=request.data)

        if serializer.is_valid():
            order = get_object_or_404(Order, id=serializer.validated_data['order'].id)
            product = get_object_or_404(Product, id=serializer.validated_data['product'].id)

            if serializer.validated_data['amount'] > product.amount:
                return Response(
                    {
                        "success": False,
                        "message": "Amount cannot be greater than product amount!"
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            if serializer.validated_data['discount'] > product.max_discount:
                return Response(
                    {
                        "success": False,
                        "message": "Discount cannot be greater than product's max discount!"
                    }
                )

            product.amount -= serializer.validated_data['amount']
            product.save()

            total = serializer.validated_data['amount'] * product.export_price * (
                    100 - serializer.validated_data['discount']) / 100
            order.total += total
            order.save()

            serializer.save(branch=self.request.user.branch, total=total)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return OrderProductSerializer
        return OrderProductPostSerializer

    def perform_destroy(self, instance):
        product = get_object_or_404(Product, id=instance.product.id)
        product.amount += instance.amount
        product.save()

        order = get_object_or_404(Order, id=instance.order.id)
        order.total -= instance.total
        order.save()

        instance.delete()

    def get_object(self):
        return get_object_or_404(OrderProduct, pk=self.kwargs['pk'], branch=self.request.user.branch)


class OrderServiceListCreateAPIView(APIView):
    permission_classes = (IsStaffStatus,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by Order ID',
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request):
        order_services = OrderService.objects.filter(branch=self.request.user.branch)

        filter_order_id = request.query_params.get('order_id', None)
        if filter_order_id is not None:
            order_services = order_services.filter(order_id=filter_order_id)

        search = request.query_params.get('search', None)
        if search is not None:
            order_services = order_services.filter(
                Q(order__customer__first_name__icontains=search) |
                Q(order__customer__last_name__icontains=search) |
                Q(service__name__icontains=search)
            )

        serializer = OrderServiceSerializer(order_services, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=OrderServicePostSerializer,
    )
    def post(self, request):
        serializer = OrderServicePostSerializer(data=request.data)
        if serializer.is_valid():
            order = get_object_or_404(Order, id=serializer.validated_data['order'].id)
            service = get_object_or_404(Service, id=serializer.validated_data['service'].id)
            worker = get_object_or_404(User, id=serializer.validated_data['worker'].id)

            total = service.price * serializer.validated_data.get('part')
            order.total += total
            order.save()

            worker.balance += total
            worker.save()

            serializer.save(branch=self.request.user.branch, total=total)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = OrderService.objects.all()
    serializer_class = OrderServiceSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return OrderServiceSerializer
        return OrderServicePostSerializer

    def perform_destroy(self, instance):
        order = get_object_or_404(Order, id=instance.order.id)

        order.total -= instance.total
        order.save()

        worker = instance.worker
        if worker is not None:
            worker.balance -= instance.total
            worker.save()

        instance.delete()

    def perform_update(self, serializer):
        order_service = self.get_object()

        previous_total = order_service.total

        updated_product_service = serializer.save()

        if updated_product_service.worker:
            total_difference = updated_product_service.total - previous_total
            updated_product_service.worker.balance += total_difference
            updated_product_service.worker.save()

    def get_object(self):
        return get_object_or_404(OrderService, pk=self.kwargs['pk'], branch=self.request.user.branch)


class SalaryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return SalarySerializer
        return SalaryPostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch, employee__role__in=['Staff', 'Manager', 'Worker']).order_by('id')

    def perform_create(self, serializer):
        employee = serializer.validated_data['employee']
        salary_amount = serializer.validated_data['amount']

        # Check if employee's balance is greater than or equal to the salary amount
        if employee.balance < salary_amount:
            return Response(
                {"detail": "The employee's balance is insufficient to add this salary."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee.balance -= salary_amount
        employee.save()

        # If validation passes, save the salary data
        serializer.save(branch=self.request.user.branch)
