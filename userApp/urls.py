from django.urls import path

from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),

    path('', UserListCreateView.as_view()),
    path('me/', UserRetrieveUpdateDestroyAPIView.as_view()),

    path('staff/', StaffListCreateView.as_view()),
    path('staff/<int:pk>/', StaffRetrieveUpdateDestroyAPIView.as_view()),

]
