from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import *
from rest_framework.permissions import *
from django.shortcuts import get_object_or_404

from userApp.permissions import *
from .serializers import *
from .models import *


class BranchesListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsSuperUser,)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CustomerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAdminUser,)

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

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
    permission_classes = (IsAdminUser,)

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self):
        queryset = self.queryset.filter(branch=self.request.user.branch)
        return get_object_or_404(queryset, pk=self.kwargs['pk'])


class CarListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAdminUser,)

    queryset = Car.objects.all()
    serializer_class = CarSerializer

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
