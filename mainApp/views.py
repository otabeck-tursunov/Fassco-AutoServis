from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from userApp.permissions import *
from .serializers import *
from .models import *
from AutoServis.paginations import *


class BranchesListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Branch.objects.all().order_by('id')
    serializer_class = BranchSerializer


class BranchRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CustomerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Customer.objects.all().order_by('id')
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
        else:
            queryset = queryset.order_by('id')

        return queryset


class CustomerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class CarListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer
    filter_backends = [SearchFilter]
    search_fields = ['code', 'name', 'brand', 'color', 'state_number', 'customer__first_name', 'customer__last_name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarSerializer
        return CarPostSerializer

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
        else:
            queryset = queryset.order_by('id')

        customer_id = self.request.query_params.get('customer_id', None)
        if customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)

        color_filter = self.request.query_params.get('color', None)
        if color_filter is not None:
            queryset = queryset.filter(color=color_filter)

        return queryset


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return CarSerializer
        else:
            return CarPostSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ProviderListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Provider.objects.all().order_by('id')
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
        else:
            queryset = queryset.order_by('id')

        debt_filter = self.request.query_params.get('debt', None)
        if debt_filter is not None:
            if debt_filter == 'true':
                queryset = queryset.filter(debt__gt=0)
            elif debt_filter == 'false':
                queryset = queryset.filter(debt=0)

        return queryset


class ProviderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ProductListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['code', 'name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductPostSerializer

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='import_required',
                description="There is little left in the warehouse. Import required!",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,

            ),
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

        import_required = self.request.query_params.get('import_required', None)
        if import_required is not None:
            if import_required == 'true':
                queryset = queryset.filter(amount__lte=models.F('min_amount'))

        order_by = self.request.query_params.get('order_by', None)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        else:
            queryset = queryset.order_by('id')

        return queryset


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductPostSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class ImportProductListCreateAPIView(APIView):
    permission_classes = (IsStaffStatus,)
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['amount', 'import_price', 'total', 'debt', 'created_at', '-created_at']
            ),
            openapi.Parameter(
                name='provider_id',
                description="Filter by Provider ID",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name='product_id',
                description="Filter by Product ID",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name='page',
                description="A page number within the paginated result set.",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name='page_size',
                description='Number of results to return per page.',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request):
        import_products = ImportProduct.objects.filter(branch=request.user.branch).order_by('id')

        search = self.request.query_params.get('search', None)
        if search is not None:
            import_products = import_products.filter(
                Q(product__name__icontains=search) |
                Q(provider__name__icontains=search)
            )

        filter_provider_id = request.query_params.get('provider_id', None)
        if filter_provider_id is not None:
            import_products = import_products.filter(provider_id=filter_provider_id)

        filter_product_id = request.query_params.get('product_id', None)
        if filter_product_id is not None:
            import_products = import_products.filter(product_id=filter_product_id)

        order_by = request.query_params.get('order_by', None)
        if order_by is not None:
            import_products = import_products.order_by(order_by)
        else:
            import_products = import_products.order_by('id')

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(import_products, request)
        serializer = ImportProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=ImportProductPostSerializer,
    )
    def post(self, request):
        serializer = ImportProductPostSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(pk=serializer.validated_data['product'].id)

            product.amount += serializer.validated_data['amount']
            product.import_price = serializer.validated_data['import_price']
            product.provider = serializer.validated_data['provider']
            product.save()

            provider = Provider.objects.get(pk=serializer.validated_data['provider'].id)
            provider.debt += serializer.validated_data['debt']
            provider.save()

            total = serializer.validated_data['amount'] * serializer.validated_data['import_price']
            serializer.save(branch=request.user.branch, total=total)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImportProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = ImportProduct.objects.all()
    serializer_class = ImportProductSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'DELETE':
            return ImportProductSerializer
        return ImportProductPostSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        instance = self.get_object()

        old_debt = instance.debt

        serializer.save()
        new_debt = serializer.validated_data.get('debt', instance.debt)

        debt_difference = new_debt - old_debt

        provider = instance.provider
        provider.debt += debt_difference
        provider.save()


class ServiceListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Service.objects.all().order_by('id')
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
        else:
            queryset = queryset.order_by('id')

        return queryset


class ServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class GetWalletAPIView(APIView):
    permission_classes = (IsStaffStatus,)

    def get(self, request):
        if Wallet.objects.exists():
            wallet = Wallet.objects.last()
        else:
            wallet = Wallet.objects.create(balance=0)

        branch = request.user.branch
        wallet.balance += branch.balance
        branch.balance = 0
        branch.save()
        wallet.save()

        return Response(data={'success': True})