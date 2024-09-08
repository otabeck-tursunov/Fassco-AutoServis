from django.urls import path
from .views import *

urlpatterns = [
    path('branches/', BranchesListCreateAPIView.as_view()),
    path('branches/<int:pk>/', BranchRetrieveUpdateDestroyAPIView.as_view()),

    path('customers/', CustomerListCreateAPIView.as_view()),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view()),

    path('cars/', CarListCreateAPIView.as_view()),
    path('cars/<int:pk>/', CarRetrieveUpdateDestroyAPIView.as_view()),

    path('providers/', ProviderListCreateAPIView.as_view()),
    path('providers/<int:pk>/', ProviderRetrieveUpdateDestroyAPIView.as_view()),

    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()),

    path('import-products/', ImportProductListCreateAPIView.as_view()),
    path('import-products/<int:pk>/', ImportProductRetrieveUpdateDestroyAPIView.as_view()),

    path('services/', ServiceListCreateAPIView.as_view()),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view()),

    path('get-wallet/', GetWalletAPIView.as_view()),

]
