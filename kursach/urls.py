
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from .views import (
    reservation_form, personal_cab, reservation_success,
    DiningTableListView, BookingListView,
    BookingDetailView,client_reservations,
    ComplexDiningTableSearchView, BookingViewSet,
 # Импортируем новое представление
)


router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personal_cab/', personal_cab, name='personal_cab'),
    path('', reservation_form, name='reservation_form'),
    path('success/', reservation_success, name='reservation_success'),
    path('api/tables/', DiningTableListView.as_view(), name='dining_table_list'),
    #path('api/bookings/', BookingListView.as_view(), name='booking_list'),
    #path('api/bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('api/tables/search/', ComplexDiningTableSearchView.as_view(), name='complex_dining_table_search'),
    path('personal_cab/<int:client_id>/', client_reservations, name='client_reservations'),
    path('api/', include(router.urls)),
]
