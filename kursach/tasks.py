from celery import shared_task
from .models import Booking
from django.utils.timezone import now
from datetime import timedelta

@shared_task
def clean_old_bookings():
    """Удаляет бронирования старше месяца"""
    month_ago = now() - timedelta(days=30)
    deleted_count, _ = Booking.objects.filter(booking_datetime__lt=month_ago).delete()
    return f"{deleted_count} старых бронирований удалено."

@shared_task
def send_booking_reminders():
    """Отправляет напоминания о бронированиях"""
    upcoming_bookings = Booking.objects.filter(
        booking_datetime__date=now().date() + timedelta(days=1)
    )
    for booking in upcoming_bookings:
        # Логика отправки напоминания (замените на send_email)
        print(f"Напоминание отправлено клиенту: {booking.client.email}")
    return f"Отправлено {len(upcoming_bookings)} напоминаний."
