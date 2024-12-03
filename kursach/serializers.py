from rest_framework import serializers
from .models import Client, DiningTable, Booking
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class DiningTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiningTable
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_email = serializers.EmailField(write_only=True)
    client_first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    client_last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    client_phone_number = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client',
            'client_email',
            'client_first_name',
            'client_last_name',
            'client_phone_number',
            'table',
            'booking_datetime',
            'status',
            'duration_of_booking',
        ]
        read_only_fields = ['booking_id', 'client']

    def validate_booking_datetime(self, value):
        # Приводим текущее время к нужной временной зоне)
        now = datetime.now(tz=value.tzinfo) if value.tzinfo else datetime.now()
        if value < now:
            raise ValidationError('Нельзя бронировать на прошедшие даты')

        booking_hour = value.hour
        if booking_hour < 9:
            raise ValidationError("Время бронирования не может быть раньше 09:00.")
        if booking_hour > 23:
            raise ValidationError("Время бронирования не может быть позже 23:00.")
        return value

    def validate_duration_of_booking(self, value):
        if value < 0:
            raise ValidationError('Длительность бронирования не может быть отрицательной.')
        elif value > 4:
            raise ValidationError('Длительность бронирования не может превышать 4 часа, согасно правилам Ресторана.')
        return value

    def validate_client_first_name(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError('Имя клиента не должно содержать цифры.')
        return value

    def validate_client_last_name(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError('Фамилия клиента не должна содержать цифры.')
        return value












#создаем нового клиента при бронировании если его не существует
    def create(self, validated_data):
        client_email = validated_data.pop('client_email')
        client_first_name = validated_data.pop('client_first_name', '')
        client_last_name = validated_data.pop('client_last_name', '')
        client_phone_number = validated_data.pop('client_phone_number', '')

        client, created = Client.objects.get_or_create(
            email=client_email,
            defaults={
                'first_name': client_first_name,
                'last_name': client_last_name,
                'phone_number': client_phone_number,
            }
        )

        # Если клиент уже существует, обновляем информацию при необходимости
        if not created:
            client.first_name = client_first_name or client.first_name
            client.last_name = client_last_name or client.last_name
            client.phone_number = client_phone_number or client.phone_number
            client.save()

        # Создание бронирования
        booking = Booking.objects.create(client=client, **validated_data)
        booking.clean()  # Вызов метода clean для валидации
        booking.save()
        return booking