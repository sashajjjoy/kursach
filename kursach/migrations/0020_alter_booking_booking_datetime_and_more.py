# Generated by Django 5.1.2 on 2024-11-30 17:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kursach', '0019_alter_booking_booking_datetime_historicalbooking_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 30, 17, 29, 39, 447555, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='historicalbooking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 30, 17, 29, 39, 447555, tzinfo=datetime.timezone.utc)),
        ),
    ]
