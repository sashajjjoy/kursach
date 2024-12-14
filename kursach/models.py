from django.db import models
from django.contrib import admin
from django.utils import timezone
import pytz
from simple_history.models import HistoricalRecords

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
        #verbose
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"

#Это позволяет удобно отображать объекты моделей в админке и других местах.
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Пример дополнительной логики: автоматически капитализируем имена
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)  # Вызов родительского метода

class DiningTable(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_number = models.IntegerField(unique=True)
    seating_capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='table_images/', blank=True, null=True,
    verbose_name="Изображение")  # Новое поле ImageField
    history = HistoricalRecords()
    @admin.display(description='Описание столика')
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

class BookingManager(models.Manager):
    def confirmed(self):
        return self.filter(status=BookingStatus.CONFIRMED)

class Booking(models.Model):
    objects = BookingManager()
    booking_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    table = models.ForeignKey(DiningTable, on_delete=models.CASCADE, related_name='bookings')
    #datatime
    booking_datetime = models.DateTimeField(default=timezone.now().astimezone(pytz.timezone('Europe/Moscow')))
    #позволяет ограничить возможные значения поля.
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    duration_of_booking = models.IntegerField(default=2)
    history = HistoricalRecords()

    class Meta:
        db_table = 'booking'
        unique_together = ('booking_datetime', 'table')
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['booking_datetime'] # Сортировка по дате и времени

    def __str__(self):
        return f"Бронирование {self.booking_id} для {self.client} в {self.table} на {self.duration_of_booking}  {self.booking_datetime}"