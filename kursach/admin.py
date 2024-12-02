from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Client, Booking, DiningTable
from simple_history.admin import SimpleHistoryAdmin
from django.utils import timezone
from datetime import timedelta


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client

    def get_export_queryset(self):
        # Экспортируем только клиентов, у которых есть бронирования за последние 30 дней
        last_30_days = timezone.now() - timedelta(days=30)
        active_clients = Booking.objects.filter(booking_datetime__gte=last_30_days).values_list('client', flat=True)
        return super().get_export_queryset().filter(pk__in=active_clients)

class BookingResource(resources.ModelResource):
    class Meta:
        model = Booking
        # Удаляем временную зону из datetime
    def dehydrate_booking_datetime(self, booking):
        return booking.booking_datetime.replace(tzinfo=None)

class DiningTableResource(resources.ModelResource):
    class Meta:
        model = DiningTable

    def get_seating_capacity(self, dining_table):
        return f"Вместимость: {dining_table.seating_capacity} человек"

class ClientAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ClientResource
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

class BookingAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = BookingResource
    list_filter = ('status',)
    date_hierarchy = 'booking_datetime'
    readonly_fields = ('booking_id',)
    list_display = ('booking_id', 'client', 'table', 'booking_datetime', 'status')
    list_display_links = ('client', 'table')
    raw_id_fields = ('client', 'table')

class DiningTableAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = DiningTableResource
    list_display = ('table_number', 'seating_capacity', 'short_description')


admin.site.register(Client, ClientAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(DiningTable, DiningTableAdmin)
