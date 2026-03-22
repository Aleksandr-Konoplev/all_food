from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User


class Table(models.Model):
    """ Модель стола """

    num_table = models.PositiveIntegerField(verbose_name='Номер столика', unique=True, validators=[MaxValueValidator(6)])
    num_of_seats = models.PositiveIntegerField(verbose_name='Максимальное количество посадочных мест')
    description = models.CharField(verbose_name='Описание столика', max_length=400)
    min_deposit = models.PositiveIntegerField(verbose_name='Минимальная сумма депозита', validators=[MaxValueValidator(50000)])

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f'Стол: {self.num_table}, Мест: {self.num_of_seats}'


class Reservation(models.Model):
    """ 
    Модель бронирование столика. Можно выбрать один из 6 столиков, добавить к брони заказ.
    client: клиент осуществивший бронирование
    table: забронированный стол (1 из 6)
    deposit: сумма депозита за столик
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь совершивший бронирование')

    start_at = models.DateTimeField(verbose_name='Начало бронирования')
    end_at = models.DateTimeField(verbose_name='Конец бронирования')
    table = models.ForeignKey(Table, verbose_name='Номер столика', on_delete=models.CASCADE)
    deposit = models.PositiveIntegerField(verbose_name='Сумма депозита', validators=[MaxValueValidator(50000)])

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'{self.owner} - {self.table}'

    def clean(self):
        super().clean()

        # Депозит всегда должен совпадать с минимальным депозитом выбранного столика.
        if self.table:
            self.deposit = self.table.min_deposit

        # ----- Ищем пересечения времени бронирования по выбранному столику с уже существующими бронями -----
        if self.table and self.start_at and self.end_at:
            overlapping = Reservation.objects.filter(
                table=self.table,
                start_at__lt=self.end_at,
                end_at__gt=self.start_at,
            )

            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError({
                    "table": "Этот столик уже забронирован на выбранное время."
                })
        # ---------------------------------------------------------------------------------------------------
