# Generated by Django 5.1.2 on 2024-11-03 20:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kursach', '0014_alter_booking_booking_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 20, 0, 29, 434654, tzinfo=datetime.timezone.utc)),
        ),
    ]
