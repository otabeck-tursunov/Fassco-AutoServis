from django.urls import path
from .views import *

urlpatterns = [
    path('expense-types/', ExpenseTypeListCreateView.as_view()),
    path('expense-types/<int:pk>/', ExpenseTypeRetrieveUpdateDestroyView.as_view()),

    path('expenses/', ExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDestroyView.as_view()),

    path('orders/', OrderListCreateAPIView.as_view()),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view()),

    path('order-products/', OrderProductListCreateAPIView.as_view()),
    path('order-products/<int:pk>/', OrderProductRetrieveUpdateDestroyAPIView.as_view()),

    path('order-services/', OrderServiceListCreateAPIView.as_view()),
    path('order-services/<int:pk>/', OrderServiceRetrieveUpdateDestroyAPIView.as_view()),

    path('salaries/', SalaryListCreateAPIView.as_view()),

]
