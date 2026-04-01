from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from table_reservation.models import Reservation


class Command(BaseCommand):
    help = 'Resets default data tables and loads project fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Run without confirmation prompt',
        )

    def handle(self, *args, **options):
        has_reservations = Reservation.objects.exists()

        tables_to_reset = [
            'auth_group_permissions',
            'auth_group',
            'core_contentforsite',
        ]
        fixtures_to_load = [
            'core/fixtures/default_groups.json',
            'core/fixtures/default_content_for_site.json',
        ]

        if has_reservations:
            self.stdout.write(
                self.style.WARNING(
                    'Reservations exist, skipping table reset and fixture load for restaurant tables.'
                )
            )
        else:
            tables_to_reset.append('table_reservation_table')
            fixtures_to_load.insert(1, 'core/fixtures/default_table.json')

        self.stdout.write(self.style.WARNING('The following tables will be truncated:'))
        for table_name in tables_to_reset:
            self.stdout.write(f'- {table_name}')

        self.stdout.write(self.style.WARNING('The following fixtures will be loaded:'))
        for fixture_path in fixtures_to_load:
            self.stdout.write(f'- {fixture_path}')

        if not options['yes']:
            confirm = input('Type "YES" to continue: ').strip().upper()
            if confirm != 'YES':
                self.stdout.write(self.style.ERROR('Operation cancelled'))
                return

        with transaction.atomic():
            self._truncate_tables(tables_to_reset)
            for fixture_path in fixtures_to_load:
                call_command('loaddata', fixture_path)

        self.stdout.write(self.style.SUCCESS('Default data loaded successfully'))

    def _truncate_tables(self, table_names):
        quoted_tables = ', '.join(connection.ops.quote_name(table_name) for table_name in table_names)
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {quoted_tables} RESTART IDENTITY CASCADE;')
