import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from table_reservation.models import Reservation, Table


class Command(BaseCommand):
    help = 'Очищает бронирования и столы, сбрасывает автоинкремент и загружает столы из JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='core/fixtures/tables.json',
            help='Путь к JSON-файлу со списком столов',
        )

    def handle(self, *args, **options):
        file_path = Path(options['path']).resolve()
        if not file_path.exists():
            raise CommandError(f'JSON-файл не найден: {file_path}')

        try:
            payload = json.loads(file_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            raise CommandError(f'Некорректный JSON в файле {file_path}: {exc}') from exc

        if not isinstance(payload, list) or not payload:
            raise CommandError('JSON должен содержать непустой список столов.')

        tables = []
        required_fields = {'num_table', 'num_of_seats', 'description'}
        for index, item in enumerate(payload, start=1):
            if not isinstance(item, dict):
                raise CommandError(f'Элемент #{index} должен быть объектом JSON.')

            missing_fields = required_fields - item.keys()
            if missing_fields:
                missing_fields_str = ', '.join(sorted(missing_fields))
                raise CommandError(f'В элементе #{index} отсутствуют поля: {missing_fields_str}.')

            tables.append(
                Table(
                    num_table=item['num_table'],
                    num_of_seats=item['num_of_seats'],
                    description=item['description'],
                )
            )

        reservation_table = connection.ops.quote_name(Reservation._meta.db_table)
        table_table = connection.ops.quote_name(Table._meta.db_table)
        reservation_count = Reservation.objects.count()
        table_count = Table.objects.count()

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE {reservation_table}, {table_table} RESTART IDENTITY;')
            Table.objects.bulk_create(tables)

        self.stdout.write(
            self.style.WARNING(
                f'Удалено бронирований: {reservation_count}. Удалено столов: {table_count}. Автоинкремент сброшен.'
            )
        )
        self.stdout.write(self.style.SUCCESS(f'Загружено столов: {len(tables)} из {file_path}'))
