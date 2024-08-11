from django.db.models import Q
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from .permissions import IsSuperUser
from .serializers import *
from .models import *


class UserListCreateView(APIView):
    permission_classes = (IsSuperUser,)

    def get(self, request):
        users = User.objects.filter(branch=request.user.branch)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(branch=request.user.branch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffListCreateView(ListCreateAPIView):
    permission_classes = (IsSuperUser,)
    queryset = User.objects.filter(
        Q(is_staff=True) | Q(role='Staff')
    )
    serializer_class = StaffSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'position')
    ordering_fields = ('username', 'first_name', 'last_name', 'position')

    def perform_create(self, serializer):
        serializer.save(role='Staff', branch=self.request.user.branch)


class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    queryset = User.objects.filter(
        Q(is_staff=True) | Q(role='Staff')
    )
    serializer_class = StaffSerializer
