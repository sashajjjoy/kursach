from django import forms

class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, label='Номер телефона')
    number_of_people = forms.IntegerField(min_value=1, label='Количество человек')
    date = forms.DateField(widget=forms.SelectDateWidget, label='Дата')
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label='Время')
    duration_of_booking = forms.IntegerField(min_value=1, label='Длительность посещения')