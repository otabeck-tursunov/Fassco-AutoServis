from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import *
from django.shortcuts import get_object_or_404

from .permissions import *
from .serializers import *
from .models import *


class UserListCreateView(ListCreateAPIView):
    permission_classes = (IsSuperUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.branch)

    def get_queryset(self):
        queryset = self.queryset.filter(branch=self.request.user.branch).order_by('username')
        return queryset
