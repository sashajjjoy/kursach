
import django_filters
from .models import Booking

class BookingFilter(django_filters.FilterSet):
    client_first_name = django_filters.CharFilter(field_name='client__first_name', lookup_expr='icontains')
    client_last_name = django_filters.CharFilter(field_name='client__last_name', lookup_expr='icontains')
    table_number = django_filters.NumberFilter(field_name='table__table_number')
    booking_date = django_filters.DateFilter(field_name='booking_datetime', lookup_expr='date')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')  # Нечувствительный к регистру


class Meta:
        model = Booking
        fields = ['client_first_name', 'client_last_name', 'table_number', 'booking_date', 'number_of_people']