
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.decorators import action
from rest_framework.response import Response
import pytz
from rest_framework import generics, viewsets, status
from .models import Client, DiningTable, Booking
from .serializers import ClientSerializer, DiningTableSerializer, BookingSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookingFilter


class ClientListView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DiningTableListView(generics.ListAPIView):
    queryset = DiningTable.objects.all()
    serializer_class = DiningTableSerializer

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]  # Разрешить доступ всем для создания бронирований

class BookingDetailView(generics.RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ComplexDiningTableSearchView(generics.ListAPIView):
    serializer_class = DiningTableSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Начинаем с полного queryset
        queryset = DiningTable.objects.all()

        # Получаем параметры из запроса
        seating_capacity_gte = self.request.query_params.get('seating_capacity__gte', None)
        description_icontains = self.request.query_params.get('description__icontains', None)

        q_objects = Q()  # Начинаем с пустого Q объекта

        # Фильтрация по вместимости (AND)
        if seating_capacity_gte is not None:
            try:
                seating_capacity_gte = int(seating_capacity_gte)
                q_objects &= Q(seating_capacity__gte=seating_capacity_gte)  # AND условие
            except ValueError:
                raise ValidationError("Параметр 'seating_capacity__gte' должен быть целым числом.")

        # Фильтрация по описанию (AND)
        if description_icontains is not None:
            q_objects &= Q(description__icontains=description_icontains)  # AND условие

        # Применяем фильтрацию к queryset
        queryset = queryset.filter(q_objects)

        # Для отладки выводим запрос SQL
        print(queryset.query)  # Чтобы проверить какой SQL-запрос будет выполнен

        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        return Response({"results": list(queryset.values())})


def reservation_form(request):
    if request.method == 'POST':
        # Получение данных из формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        number_of_people = request.POST.get('number_of_people')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration_of_booking = request.POST.get('duration_of_booking')
        status=request.POST.get('status')

        if not all([first_name, last_name, email, phone, number_of_people, date, time, status]):
            return render(request, 'reservation_form.html', {
                'error': 'Пожалуйста, заполните все поля.'
            })

        try:
            booking_datetime_str = f"{date} {time}"
            booking_datetime = timezone.make_aware(
                timezone.datetime.strptime(booking_datetime_str, "%Y-%m-%d %H:%M"),
                timezone=pytz.timezone('Europe/Moscow')
            )
        except ValueError:
            return render(request, 'reservation_form.html', {
                'error': 'Неверный формат даты или времени.'
            })


        client, created = Client.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone,
            }
        )
        if not created:
            client.first_name = first_name
            client.last_name = last_name
            client.phone_number = phone
            client.save()

        # Автоматический выбор доступного столика
        try:
            number_of_people = int(number_of_people)
            tables = DiningTable.objects.filter(seating_capacity__gte=number_of_people).order_by('seating_capacity')
            table = None
            for t in tables:
                # Проверяем, свободен ли столик на выбранное время
                if not Booking.objects.filter(table=t, booking_datetime=booking_datetime).exists():
                    table = t
                    break
            if not table:
                return render(request, 'reservation_form.html', {
                    'error': 'К сожалению, нет доступных столиков на выбранное время.'
                })
        except ValueError:
            return render(request, 'reservation_form.html', {
                'error': 'Неверное количество человек.'
            })

        # Создание бронирования
        try:

            booking = Booking.objects.create(
                client=client,
                table=table,
                booking_datetime=booking_datetime,
                status='Pending',
                duration_of_booking = duration_of_booking
            )
            booking.clean()
        except IntegrityError:
            return render(request, 'reservation_form.html', {
                'error': 'Этот столик уже забронирован на выбранное время.'
            })

        # Перенаправление на страницу успеха
        return redirect('reservation_success')

    else:
        # Если метод GET, просто отобразить форму
        return render(request, 'reservation_form.html')

def client_reservations(request, client_id):
    # Получение клиента по ID
    client = get_object_or_404(Client, id=client_id)

    # Получаем все бронирования конкретного клиента
    bookings = Booking.objects.filter(client=client)

    # Фильтрация по параметрам запроса
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    table_number = request.GET.get('table_number')
    booking_date = request.GET.get('booking_date')
    people_count = request.GET.get('people_count')

    # Создаём Q объект для накопления фильтров
    filters = Q()

    if first_name:
        filters &= Q(client__first_name__icontains=first_name)
    if last_name:
        filters &= Q(client__last_name__icontains=last_name)
    if table_number:
        filters &= Q(table__table_number=table_number)
    if booking_date:
        filters &= Q(booking_datetime__date=booking_date)
    if people_count:
        filters &= Q(duration_of_booking=people_count)

    # Применяем фильтры к бронированиям
    bookings = bookings.filter(filters)

    # Передаём бронирования в шаблон
    context = {
        'client': client,
        'bookings': bookings,
        'first_name': first_name,
        'last_name': last_name,
        'table_number': table_number,
        'booking_date': booking_date,
        'people_count': people_count,
    }
    return render(request, 'personal_cab.html', context)

def reservation_success(request):
    return render(request, 'reservation_success.html')

def personal_cab(request):
    return render(request, 'personal_cab.html')

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('booking_datetime')
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BookingFilter  # Временно закомментируйте эту строку
    search_fields = [
        'client__first_name',
        'client__last_name',
        'client__email',
        'status',
        'table__table_number'
    ]
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=True)
    def update_booking_status(self, request, pk=None):
        """Обновляет статус бронирования."""
        booking = self.get_object()
        status_data = request.data.get('status')

        if not status_data:
            return Response({'error': 'Статус должен быть предоставлен.'},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = status_data
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def week(self, request):
        """Возвращает бронирования на следующую неделю."""
        today = timezone.now()
        start_of_next_week = today + timezone.timedelta(
            days=(7 - today.weekday() % 7))  # Начало следующей недели (понедельник)
        end_of_next_week = start_of_next_week + timezone.timedelta(days=7)  # Конец следующей недели

        upcoming_bookings = self.queryset.filter(
            booking_datetime__gte=start_of_next_week,
            booking_datetime__lt=end_of_next_week
        )

        serializer = self.get_serializer(upcoming_bookings, many=True)
        return Response(serializer.data)