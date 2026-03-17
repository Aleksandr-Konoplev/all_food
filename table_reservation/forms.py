from django import forms

from table_reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('start_at', 'end_at', 'table', 'deposit')
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'class': 'form-control', 'step': 900}, format="%Y-%m-%dT%H:%M",),
            'end_at': forms.DateTimeInput(attrs={'class': 'form-control', 'step': 900}, format="%Y-%m-%dT%H:%M",),
            'table': forms.Select(attrs={'class': 'form-select'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 500}),
        }

    def clean_start_at(self):
        """ Проверка выбранного времени кратности 15 минутам """
        value = self.cleaned_data["start_at"]
        if value.minute % 15 != 0 or value.second != 0 or value.microsecond != 0:
            raise forms.ValidationError("Время начала должно быть кратно 15 минутам.")
        return value

    def clean_end_at(self):
        """ Проверка выбранного времени кратности 15 минутам """
        value = self.cleaned_data["end_at"]
        if value.minute % 15 != 0 or value.second != 0 or value.microsecond != 0:
            raise forms.ValidationError("Время окончания должно быть кратно 15 минутам.")
        return value

    def clean(self):
        """ Проверка корректности введенных времени (время начала брони не может быть позже времени окончания брони)"""
        cleaned_data = super().clean()
        start_at = cleaned_data.get("start_at")
        end_at = cleaned_data.get("end_at")
        if start_at and end_at and end_at <= start_at:
            raise forms.ValidationError("Время окончания должно быть позже времени начала.")
        return cleaned_data
