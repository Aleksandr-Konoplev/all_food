from django import forms

from table_reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('start_at', 'end_at', 'table', 'deposit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_at'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Выберите дату и время начала брони', 'step': 900}
        )
        self.fields['end_at'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Выберите дату и время окончания брони', 'step': 900}
        )
        self.fields['table'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Выберите стол'}
        )
        self.fields['deposit'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Укажите депозит'}
        )

    def clean_start_at(self):
        """ Проверка выбранного времени начала брони. """
        value = self.cleaned_data['start_at']
        if value.minute % 15 != 0:
            raise forms.ValidationError('Время начала должно быть кратно 15 минутам.')
        if value.hour < 10:
            raise forms.ValidationError('Мы открываемся в 10:00')
        if value.hour >= 21:
            raise forms.ValidationError('После 21:00 бронирования не принимаются')
        return value

    def clean_end_at(self):
        """ Проверка выбранного времени окончания брони. """
        value = self.cleaned_data['end_at']
        if value.minute % 15 != 0:
            raise forms.ValidationError('Время окончания должно быть кратно 15 минутам.')
        if value.day > self.cleaned_data['start_at'].day:
            raise forms.ValidationError('Мы закрываемся в 00:00.')
        return value

    def clean(self):
        """ Проверка корректности введенных времени (время начала брони не может быть позже времени окончания брони). """
        cleaned_data = super().clean()
        start_at = cleaned_data.get('start_at')
        end_at = cleaned_data.get('end_at')
        if start_at and end_at and end_at <= start_at:
            raise forms.ValidationError('Время окончания должно быть позже времени начала.')
        return cleaned_data
