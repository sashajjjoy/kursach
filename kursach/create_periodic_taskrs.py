from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from kursach.tasks import clean_old_bookings, send_booking_reminders

class Command(BaseCommand):
    help = "Создает периодические задачи для Celery"

    def handle(self, *args, **kwargs):
        # Создаем расписание каждые 10 минут
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.MINUTES
        )

        # Создаем задачу для очистки старых бронирований
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Очистка старых бронирований',
            task='kursach.tasks.clean_old_bookings'
        )

        # Создаем задачу для напоминаний о бронированиях
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Напоминания о бронированиях',
            task='kursach.tasks.send_booking_reminders'
        )

        self.stdout.write(self.style.SUCCESS('Периодические задачи успешно созданы'))
