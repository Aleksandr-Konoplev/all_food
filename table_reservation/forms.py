from django import forms

from table_reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        # Поле депозита скрыто из формы, так как его значение всегда берется из выбранного столика.
        fields = ('start_at', 'end_at', 'table')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Передаем в шаблон минимальные депозиты только для столиков, доступных в текущем queryset формы.
        self.table_deposits = {
            str(table.pk): table.min_deposit
            for table in self.fields['table'].queryset
        }

        self.fields['start_at'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Выберите дату и время начала брони', 'step': 900}
        )
        self.fields['end_at'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Выберите дату и время окончания брони', 'step': 900}
        )
        self.fields['table'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Выберите стол'}
        )

    def clean_start_at(self):
        """ Проверка выбранного времени начала брони. """
        value = self.cleaned_data.get('start_at')
        if value.minute % 15 != 0:
            raise forms.ValidationError('Время начала должно быть кратно 15 минутам.')
        if value.hour < 10:
            raise forms.ValidationError('Мы открываемся в 10:00')
        if value.hour >= 21:
            raise forms.ValidationError('После 21:00 бронирования не принимаются')
        return value

    def clean_end_at(self):
        """ Проверка выбранного времени окончания брони. """
        end_at = self.cleaned_data.get('end_at')
        start_at = self.cleaned_data.get('start_at')
        if end_at.minute % 15 != 0:
            raise forms.ValidationError('Время окончания должно быть кратно 15 минутам.')
        if start_at and end_at.day > start_at.day:
            raise forms.ValidationError('Мы закрываемся в 00:00.')
        return end_at

    def clean(self):
        """ Проверка времени и принудительная синхронизация депозита с выбранным столиком. """
        cleaned_data = super().clean()
        start_at = cleaned_data.get('start_at')
        end_at = cleaned_data.get('end_at')
        table = cleaned_data.get('table')

        if start_at and end_at and end_at <= start_at:
            raise forms.ValidationError('Время окончания должно быть позже времени начала.')
        # Депозит всегда должен быть равен минимальному депозиту выбранного столика.
        if table:
            cleaned_data['deposit'] = table.min_deposit
        return cleaned_data
