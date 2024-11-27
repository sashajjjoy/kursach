# Generated by Django 5.1.2 on 2024-10-20 13:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='DiningTable',
            fields=[
                ('table_id', models.AutoField(primary_key=True, serialize=False)),
                ('table_number', models.IntegerField(unique=True)),
                ('seating_capacity', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'dining_table',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kursach.client')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kursach.diningtable')),
            ],
            options={
                'db_table': 'booking',
                'unique_together': {('booking_datetime', 'table')},
            },
        ),
    ]
