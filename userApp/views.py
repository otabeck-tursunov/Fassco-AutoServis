from django.db.models import Q
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from .permissions import IsSuperUser, RoleIsAdmin
from .serializers import *
from .models import *


class UserListCreateView(APIView):
    permission_classes = (IsSuperUser,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(branch=self.request.user.branch)


class StaffListCreateView(ListCreateAPIView):
    permission_classes = (RoleIsAdmin,)

    queryset = User.objects.filter(
        Q(is_staff=True) | Q(role='Staff') | Q(role='Admin')
    )

    serializer_class = StaffSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'position')
    ordering_fields = ('username', 'first_name', 'last_name', 'position')

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(role='Staff', branch=self.request.user.branch)


class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (RoleIsAdmin,)

    queryset = User.objects.filter(
        Q(is_staff=True) | Q(role='Staff')
    )
    serializer_class = StaffSerializer
