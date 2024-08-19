from django.urls import path
from .views import *

urlpatterns = [
    path('top-sale-products/', TopSaleProductAPIView.as_view()),
    path('top-customers/', TopCustomersAPIView.as_view()),
    path('monthly-total/', MonthlyTotalsAPIView.as_view()),
    path('calculate/', StatisticsAPIView.as_view()),
    path('expenses/', ExpensesStatisticsAPIView.as_view()),
]
