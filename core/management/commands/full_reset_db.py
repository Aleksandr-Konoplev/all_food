from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "FULL reset for PostgreSQL (truncate, reset identity, cascade)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("POSTGRES FULL RESET"))

        confirm = input("Type 'YES' to completely wipe the database: ")
        if confirm != "YES":
            self.stdout.write(self.style.ERROR("Operation cancelled"))
            return

        tables = connection.introspection.table_names()
        if not tables:
            self.stdout.write(self.style.WARNING("No tables found"))
            return

        tables_sql = ', '.join(f'"{t}"' for t in tables)

        with connection.cursor() as cursor:
            cursor.execute(f"""
                TRUNCATE TABLE {tables_sql}
                RESTART IDENTITY CASCADE;
            """)

        self.stdout.write(self.style.SUCCESS("PostgreSQL DB reset complete"))