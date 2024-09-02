from django.template.context_processors import request
from drf_yasg.openapi import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .permissions import *
from .serializers import *
from .models import *


class ManagerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = User.objects.filter(role='Manager')
    serializer_class = ManagerSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ManagerSerializer
        return ManagerPostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(role='Manager', is_staff=True, branch=self.request.user.branch)


class ManagerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffStatus]

    queryset = User.objects.filter(role='Manager')
    serializer_class = ManagerSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ManagerSerializer
        return ManagerPostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        serializer.save(role='Manager', is_staff=True, branch=self.request.user.branch)


class WorkerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = User.objects.filter(role='Worker')
    serializer_class = WorkerSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkerSerializer
        return WorkerPostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(role='Worker', is_staff=True, branch=self.request.user.branch)


class WorkerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffStatus]

    queryset = User.objects.filter(role='Worker')
    serializer_class = WorkerSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkerSerializer
        return WorkerPostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return Response("Unauthorized!", status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        serializer.save(role='Worker', is_staff=True, branch=self.request.user.branch)


class StaffListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = User.objects.filter(role='Staff')
    serializer_class = StaffSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffSerializer
        return StaffPostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(role='Staff', is_staff=True, branch=self.request.user.branch)


class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffStatus]

    queryset = User.objects.filter(role='Staff')
    serializer_class = StaffSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffSerializer
        return StaffPostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(branch=self.request.user.branch)
        return Response("Unauthorized!", status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        serializer.save(role='Staff', is_staff=True, branch=self.request.user.branch)


class GetMeRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsStaffStatus,)

    queryset = User.objects.filter(role__in=['Manager', 'Worker', 'Staff']).order_by('id')
    serializer_class = UserSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return UserSerializer
        return UserPostSerializer

    def get_queryset(self):
        return self.queryset.filter(branch=self.request.user.branch)

    def perform_create(self, serializer):
        serializer.save(is_staff=True, branch=self.request.user.branch)


# class UserListCreateView(APIView):
#     permission_classes = (IsSuperStatus,)
#
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     @swagger_auto_schema(
#         request_body=UserSerializer,
#     )
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthenticated,)
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_object(self):
#         return self.request.user
#
#     def perform_update(self, serializer):
#         serializer.save(branch=self.request.user.branch)
#
#
# class StaffListCreateView(ListCreateAPIView):
#     permission_classes = (IsSuperStatus,)
#
#     queryset = User.objects.filter(
#         Q(is_staff=True) | Q(role='Staff') | Q(role='Admin')
#     )
#
#     serializer_class = StaffSerializer
#     filter_backends = (SearchFilter, OrderingFilter,)
#     search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'position')
#     ordering_fields = ('username', 'first_name', 'last_name', 'position')
#
#     def get_queryset(self):
#         return self.queryset.filter(branch=self.request.user.branch)
#
#     def perform_create(self, serializer):
#         serializer.save(role='Staff', branch=self.request.user.branch)
#
#
# class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsSuperStatus,)
#
#     queryset = User.objects.filter(
#         Q(is_staff=True) | Q(role='Staff')
#     )
#     serializer_class = StaffSerializer
