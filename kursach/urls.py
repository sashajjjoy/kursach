
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from .views import (
    reservation_form, personal_cab, reservation_success,
    DiningTableListView, client_reservations, BookingViewSet)


router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personal_cab/', personal_cab, name='personal_cab'),
    path('', reservation_form, name='reservation_form'),
    path('success/', reservation_success, name='reservation_success'),
    path('api/tables/', DiningTableListView.as_view(), name='dining_table_list'),
    path('personal_cab/<int:client_id>/', client_reservations, name='client_reservations'),
    path('api/', include(router.urls)),
]
