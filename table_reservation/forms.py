from django import forms

from table_reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('date_visit', 'time_visit', 'duration_visit', 'table', 'deposit')
        widgets = {
            'date_visit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_visit': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': 900}),
            'duration_visit': forms.NumberInput(attrs={'class': 'form-control', 'min': 30, 'step': 30}),
            'table': forms.Select(attrs={'class': 'form-select'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 500}),
        }

    def clean_time_visit(self):
        value = self.cleaned_data['time_visit']
        if value.minute % 15 != 0 or value.second != 0:
            raise forms.ValidationError('Время визита должно быть кратно 15 минутам.')
        return value
