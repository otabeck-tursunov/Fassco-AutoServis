from django.urls import path

from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),

    path('me/', GetMeRetrieveAPIView.as_view()),

    path('', UserListCreateAPIView.as_view()),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view()),

    path('managers/', ManagerListCreateAPIView.as_view()),
    path('managers/<int:pk>/', ManagerRetrieveUpdateDestroyAPIView.as_view()),

    path('workers/', WorkerListCreateAPIView.as_view()),
    path('workers/<int:pk>/', WorkerRetrieveUpdateDestroyAPIView.as_view()),

    path('staff/', StaffListCreateAPIView.as_view()),
    path('staff/<int:pk>/', StaffRetrieveUpdateDestroyAPIView.as_view()),

]
