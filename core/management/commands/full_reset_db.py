import psycopg2
from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Command(BaseCommand):
    help = 'Удаляет и пересоздаёт базу данных (только для dev)'

    def handle(self, *args, **options):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default'].get('HOST', 'localhost')
        db_port = settings.DATABASES['default'].get('PORT', 5432)

        # Запрос подтверждения
        confirm = input(f'Вы уверены, что хотите удалить базу "{db_name}" и создать заново? [y/N]: ')
        if confirm.lower() != 'y':
            self.stdout.write(self.style.WARNING('Операция отменена.'))
            return

        # Подключаемся к postgres (не к удаляемой базе)
        conn = psycopg2.connect(dbname="postgres", user=db_user, password=db_password, host=db_host, port=db_port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Удаляем базу, если существует
        self.stdout.write(f'Удаляем базу {db_name}...')
        # noinspection SqlNoDataSourceInspection
        cur.execute(f'DROP DATABASE IF EXISTS "{db_name}";')

        # Создаём базу заново
        self.stdout.write(f'Создаём базу {db_name}...')
        # noinspection SqlNoDataSourceInspection
        cur.execute(f'CREATE DATABASE "{db_name}";')

        cur.close()
        conn.close()
        self.stdout.write(self.style.SUCCESS(f'База {db_name} успешно пересоздана!'))
