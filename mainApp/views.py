from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import *
from rest_framework.permissions import *
from django.shortcuts import get_object_or_404

from userApp.permissions import *
from .serializers import *
from .models import *


class BranchesListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CustomerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone_number']

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['first_name', 'last_name', 'debt']
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        return queryset


class CustomerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class CarListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [SearchFilter]
    search_fields = ['code', 'name', 'brand', 'color', 'state_number']

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['code', 'name', 'state_number']
            ),
            openapi.Parameter(
                name='customer_id',
                description="Filter by Customer ID",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='color',
                description="Filter by Color",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        customer_id = self.request.query_params.get('customer_id', None)
        if customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)

        color_filter = self.request.query_params.get('color', None)
        if color_filter is not None:
            queryset = queryset.filter(color=color_filter)

        return queryset


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ProviderListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'phone_number']

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['name', 'debt']
            ),
            openapi.Parameter(
                name='debt',
                description="true: qarzdorlik bo'lgan Providerlar, false: qarzdorlik bo'lmagan Providerlar!",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        debt_filter = self.request.query_params.get('debt', None)
        if debt_filter is not None:
            if debt_filter == 'true':
                queryset = queryset.filter(debt__gt=0)
            elif debt_filter == 'false':
                queryset = queryset.filter(debt=0)

        return queryset


class ProviderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ProductListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['code', 'name']

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['name', 'code', 'amount', 'max_discount']
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        return queryset


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ImportProductListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ImportProduct.objects.all()
    serializer_class = ImportProductSerializer
    filter_backends = [SearchFilter]

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['amount', 'debt', 'created_at', '-created_at']
            ),
            openapi.Parameter(
                name='provider_id',
                description="Filter by Provider ID",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        provider_id = self.request.query_params.get('provider_id', None)
        if provider_id is not None:
            queryset = queryset.filter(provider_id=provider_id)

        return queryset


class ImportProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ImportProduct.objects.all()
    serializer_class = ImportProductSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ServiceListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['name', 'price', 'created_at', '-created_at']
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)

        return queryset


class ServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])
