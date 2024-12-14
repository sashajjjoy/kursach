from django import forms
from .models import Client

class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, label='Номер телефона')
    number_of_people = forms.IntegerField(min_value=1, label='Количество человек')
    date = forms.DateField(widget=forms.SelectDateWidget, label='Дата')
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label='Время')
    duration_of_booking = forms.IntegerField(min_value=1, label='Длительность посещения')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        if len(phone) < 10:
            raise forms.ValidationError("Номер телефона слишком короткий.")
        return phone
