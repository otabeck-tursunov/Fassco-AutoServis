from django.urls import path
from .views import *

urlpatterns = [
    path('branches/', BranchesListCreateAPIView.as_view()),
    path('branches/<int:pk>/', BranchRetrieveUpdateDestroyAPIView.as_view()),

    path('customers/', CustomerListCreateAPIView.as_view()),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view()),

    path('cars/', CarListCreateAPIView.as_view()),
]