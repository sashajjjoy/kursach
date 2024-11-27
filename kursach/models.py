from traceback import print_tb
import logging
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib import admin
from django.utils import timezone
import pytz
from simple_history.models import HistoricalRecords

from datetime import timedelta, time as datetime_time  # Правильный импорт

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    history = HistoricalRecords()
    class Meta:
        app_label = 'kursach'
        db_table = 'client'
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DiningTable(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_number = models.IntegerField(unique=True)
    seating_capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    history = HistoricalRecords()
    @admin.display(description='Описание столика')  # Короткое описание
    def short_description(self):
        return self.description or "Нет описания"

    class Meta:
        db_table = 'dining_table'
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

    def __str__(self):
        return f"Столик {self.table_number} (Вместимость: {self.seating_capacity})"



class BookingStatus(models.TextChoices):
    PENDING = 'Pending', 'Ожидает подтверждения'
    CONFIRMED = 'Confirmed', 'Подтверждено'
    CANCELLED = 'Cancelled', 'Отменено'

logger = logging.getLogger('booking_app')


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    table = models.ForeignKey(DiningTable, on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField(default=timezone.now().astimezone(pytz.timezone('Europe/Moscow')))
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    duration_of_booking = models.IntegerField(default=2)
    history = HistoricalRecords()
    def clean(self):
        moscow_timezone = pytz.timezone('Europe/Moscow')
        now = timezone.now().astimezone(moscow_timezone)
        booking_time = self.booking_datetime.time()

        if self.booking_datetime < now:
            raise ValidationError("Дата и время бронирования не могут быть в прошлом.")

        earliest_time = datetime_time(9, 0)  # 09:00
        if booking_time < earliest_time:
            raise ValidationError("Время бронирования не может быть раньше 09:00.")

        end_datetime = self.booking_datetime + timedelta(hours=int(self.duration_of_booking))
        end_time = end_datetime.time()

        latest_time = datetime_time(23, 59)
        if end_time > latest_time:
            raise ValidationError("Время окончания бронирования не может превышать полночь (00:00).")

    class Meta:
        db_table = 'booking'
        unique_together = ('booking_datetime', 'table')
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронирование {self.booking_id} для {self.client} в {self.table} на {self.duration_of_booking}  {self.booking_datetime}"