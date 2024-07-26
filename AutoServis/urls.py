from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Auto Service API",
        default_version='v1',
        description="Masuliyatli bo'ling, tushunmaganingizni so'rang. Muddat 15-avgust!",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="otabecktursunov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    path('users/', include('userApp.urls')),
    path('main/', include('mainApp.urls')),
]
