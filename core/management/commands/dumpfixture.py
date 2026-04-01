from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Кастомная команда Django для безопасной выгрузки данных из БД в JSON-фикстуру.

    Использует встроенную команду dumpdata, но записывает результат напрямую
    в файл с кодировкой UTF-8, что позволяет избежать проблем с кодировкой
    в Windows (PowerShell, cmd).
    args:
        app_model (str): Модель в формате 'app_label.ModelName'
        output (str): Путь к выходному JSON-файлу
    """

    def add_arguments(self, parser):
        """Определение аргументов командной строки."""
        parser.add_argument("app_model")
        parser.add_argument("output")

    def handle(self, *args, **options):
        """Выполняет dumpdata и сохраняет результат в файл с кодировкой UTF-8."""
        print("Если указанный файл уже существует, он будет перезаписан!")
        confirm = input('Введите "YES" для продолжения: ').strip().upper()
        if confirm != "YES":
            return

        with open(options["output"], "w", encoding="utf-8") as f:
            call_command("dumpdata", options["app_model"], indent=4, stdout=f)
