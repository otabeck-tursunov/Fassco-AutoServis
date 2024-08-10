from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticated
from rest_framework.views import APIView

from .serializers import *
from .models import *


class ExpenseTypeListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ExpenseType.objects.all().order_by('id')
    serializer_class = ExpenseTypeSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)


class ExpenseTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer

    def get_object(self):
        return get_object_or_404(ExpenseType, pk=self.kwargs['pk'], branch=self.request.user.branch)


class ExpenseListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_object(self):
        return get_object_or_404(Expense, pk=self.kwargs['pk'], branch=self.request.user.branch)


class OrderListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer

    filter_backends = [OrderingFilter, ]
    ordering_fields = '__all__'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        return OrderPostSerializer

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs['pk'], branch=self.request.user.branch)


class OrderProductListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by Order ID',
            )
        ]
    )
    def get(self, request):
        order_products = OrderProduct.objects.filter(branch=self.request.user.branch).order_by('id')

        filter_order_id = request.query_params.get('order_id', None)
        if filter_order_id is not None:
            get_object_or_404(Order, pk=filter_order_id)
            order_products = order_products.filter(order_id=filter_order_id)

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
    permission_classes = (IsAuthenticated,)

    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

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
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by Order ID',
            )
        ]
    )
    def get(self, request):
        order_services = OrderService.objects.filter(branch=self.request.user.branch)

        filter_order_id = request.query_params.get('order_id', None)
        if filter_order_id is not None:
            order_services = order_services.filter(order_id=filter_order_id)

        serializer = OrderServiceSerializer(order_services, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=OrderServiceSerializer,
    )
    def post(self, request):
        serializer = OrderServicePostSerializer(data=request.data)
        if serializer.is_valid():
            order = get_object_or_404(Order, id=serializer.validated_data['order'].id)
            service = get_object_or_404(Service, id=serializer.validated_data['service'].id)

            total = service.price * serializer.validated_data.get('part')
            order.total += total
            order.save()

            serializer.save(branch=self.request.user.branch, total=total)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = OrderService.objects.all()
    serializer_class = OrderServiceSerializer

    def perform_destroy(self, instance):
        order = get_object_or_404(Order, id=instance.order.id)

        order.total -= instance.total
        order.save()
        instance.delete()

    def get_object(self):
        return get_object_or_404(OrderService, pk=self.kwargs['pk'], branch=self.request.user.branch)
