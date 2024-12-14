
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from django.urls import path, include
from rest_framework import permissions

from drf_yasg import openapi
from .views import (
    reservation_form, personal_cab, reservation_success,
    DiningTableListView, client_reservations, BookingViewSet, ClientListView)


router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personal_cab/', personal_cab, name='personal_cab'),
    path('', reservation_form, name='reservation_form'),
    path('success/', reservation_success, name='reservation_success'),
    path('api/tables/', DiningTableListView.as_view(), name='dining_table_list'),
    path('api/clients/', ClientListView.as_view(), name='clients_list'),
    path('personal_cab/<int:client_id>/', client_reservations, name='client_reservations'),
    path('api/', include(router.urls)),
]

schema_view = get_schema_view(
    openapi.Info(
        title="API Документация",
        default_version='v1',
        description="Документация вашего API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path(r'swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]