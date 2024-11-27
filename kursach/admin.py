
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Client, Booking, DiningTable
from simple_history.admin import SimpleHistoryAdmin

class ClientResource(resources.ModelResource):
    class Meta:
        model = Client

    def dehydrate_email(self, client):
        return client.email + ' (client)'

class BookingResource(resources.ModelResource):
    class Meta:
        model = Booking

    def get_export_queryset(self):
        return super().get_export_queryset().filter(status='confirmed')

    def dehydrate_booking_id(self, booking):
        return f"Booking ID: {booking.booking_id}"

class DiningTableResource(resources.ModelResource):
    class Meta:
        model = DiningTable

    def get_seating_capacity(self, dining_table):
        return f"Capacity: {dining_table.seating_capacity}"

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
