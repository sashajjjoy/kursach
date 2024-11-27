# Generated by Django 5.1.2 on 2024-11-03 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kursach', '0009_alter_booking_options_alter_client_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='duration_of_booking',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 19, 2, 22, 199167, tzinfo=datetime.timezone.utc)),
        ),
    ]