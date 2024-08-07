from django.urls import path
from .views import *

urlpatterns = [
    path('top-sale-products/', TopSaleProductAPIView.as_view()),
]