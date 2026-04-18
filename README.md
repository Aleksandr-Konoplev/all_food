# All Food

Django-приложение для сайта ресторана: публичные страницы, регистрация пользователей с подтверждением email, обратная связь и бронирование столиков.

## Что есть в проекте

- `core` - главная страница, страница о ресторане, блоки контента, сообщения обратной связи, панель управления
- `users` - кастомная модель пользователя, вход по email, регистрация, подтверждение почты, профиль и CRUD пользователей
- `table_reservation` - столики и бронирования с проверкой пересечений по времени
- роли: пользователь, модератор, суперпользователь
- две SMTP-конфигурации: `main` для основной почты и `auto` для автоматических писем

## Стек

- Python `3.14`
- Django `6.0.3`
- PostgreSQL
- SQLite для тестового окружения
- Pillow
- python-dotenv
- psycopg2
- Gunicorn
- black, isort, flake8, coverage

Основные зависимости описаны в `pyproject.toml`, а Docker-образ собирается с установкой пакетов из `requirements.txt`.

## Структура проекта

- `config` - настройки Django, маршруты, WSGI/ASGI, тестовые настройки
- `core` - страницы сайта, контентные блоки, обратная связь, management-команды, фикстуры
- `users` - пользователи, регистрация, подтверждение email, профили
- `table_reservation` - столики, бронирования и проверка доступности
- `templates` - HTML-шаблоны
- `static` - исходная статика проекта
- `staticfiles` - собранная статика
- `media` - загружаемые файлы

## Переменные окружения

Проект загружает переменные из файла `.env`.

```env
SECRET_KEY=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
HOST=
PORT=

EMAIL_HOST_MAIN=
EMAIL_PORT_MAIN=
EMAIL_HOST_USER_MAIN=
EMAIL_HOST_PASSWORD_MAIN=
EMAIL_USE_TLS_MAIN=
EMAIL_USE_SSL_MAIN=

EMAIL_HOST_AUTO=
EMAIL_PORT_AUTO=
EMAIL_HOST_USER_AUTO=
EMAIL_HOST_PASSWORD_AUTO=
EMAIL_USE_TLS_AUTO=
EMAIL_USE_SSL_AUTO=

CSRF_TRUSTED_ORIGINS=
ALLOWED_HOSTS=
```

Примечания:

- `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` читаются как список через запятую
- `DEBUG` в текущей конфигурации захардкожен в `config/settings.py` и не читается из `.env`
- для Docker-сценария `HOST` обычно равен `db`, для локального запуска - `localhost`

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install -e .
python manage.py migrate
python manage.py load_default_data --yes
python manage.py custom_csu
python manage.py runserver
```

Проект по умолчанию использует PostgreSQL из настроек `config/settings.py`.

## Запуск через Docker

В репозитории уже есть `Dockerfile` и `docker-compose.yml`.

```bash
docker compose up --build
```

Текущая конфигурация `docker-compose.yml` делает следующее:

- поднимает сервис `db` на базе `postgres:17-alpine`
- собирает сервис `app` из локального `Dockerfile`
- выполняет `python manage.py migrate`
- выполняет `python manage.py load_default_data --yes`
- запускает Django dev-сервер на `0.0.0.0:8000`

Отдельно `Dockerfile` настроен на запуск `collectstatic` и `gunicorn`, поэтому его можно использовать и как базу для production-сценария.

## Фикстуры и начальные данные

В проекте есть стартовые фикстуры:

- `core/fixtures/default_content_for_site.json`
- `core/fixtures/default_groups.json`
- `core/fixtures/default_table.json`

Рекомендуемый способ загрузки - через management-команду:

```bash
python manage.py load_default_data --yes
```

Команда:

- очищает таблицы с группами и контентом
- загружает базовые группы и контент
- загружает столики, если в системе еще нет бронирований

При необходимости фикстуры можно загружать и вручную:

```bash
python manage.py loaddata core/fixtures/default_groups.json
python manage.py loaddata core/fixtures/default_content_for_site.json
python manage.py loaddata core/fixtures/default_table.json
```

## Основные сущности

- `users.User` - пользователь с логином по `email`, без `username`
- `core.ContentForSite` - редактируемые блоки текста и изображений
- `core.Feedback` - сообщения из формы обратной связи
- `table_reservation.Table` - столик, количество мест, описание, минимальный депозит
- `table_reservation.Reservation` - бронирование столика на заданный интервал времени

## Особенности логики

- новый пользователь создается неактивным и активируется по ссылке из email
- для модераторов используется группа `moderator`
- депозит бронирования автоматически синхронизируется с `Table.min_deposit`
- нельзя создать пересекающиеся бронирования для одного столика
- в проекте используется кастомная модель пользователя: `AUTH_USER_MODEL = users.User`
- основная база данных - PostgreSQL, а в `config/test_settings.py` для тестов используется SQLite

## Management-команды

- `python manage.py custom_csu` - создать суперпользователя для кастомной модели
- `python manage.py load_default_data --yes` - загрузить стартовые данные без интерактивного подтверждения
- `python manage.py dumpfixture core.ContentForSite core/fixtures/content_for_site.json` - выгрузить данные модели в JSON
- `python manage.py dumpfixture table_reservation.Table core/fixtures/tables.json` - выгрузить столики в JSON
- `python manage.py dumpdata auth.group --indent 2 > core/fixtures/groups.json` - выгрузить группы
- `python manage.py loaddata core/fixtures/groups.json` - загрузить группы
- `python manage.py full_reset_db` - полностью очистить PostgreSQL БД

## Маршруты

- `/admin/` - стандартная Django admin-панель
- `/` - главная страница
- `/about/` - страница о ресторане
- `/control-panel/` - панель управления
- `/content/` - список блоков контента
- `/content/<int:pk>/update/` - редактирование блока контента
- `/feedbacks/` - список сообщений обратной связи
- `/feedbacks/<int:pk>/` - детальная страница сообщения
- `/feedbacks/<int:pk>/delete/` - удаление сообщения
- `/users/login/`, `/users/logout/`, `/users/register/`
- `/users/email-confirm/<str:token>/` - подтверждение email
- `/users/list/` - список пользователей
- `/users/user/<int:pk>/detail/` - карточка пользователя
- `/users/user/<int:pk>/update/` - редактирование пользователя
- `/users/user/<int:pk>/delete/` - удаление пользователя
- `/reserve/create/`, `/reserve/list/`
- `/reserve/<int:pk>/detail/`, `/reserve/<int:pk>/update/`, `/reserve/<int:pk>/delete/`

## Статика и медиа

- `STATIC_URL = static/`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `MEDIA_URL = /media/`
- `MEDIA_ROOT = BASE_DIR / 'media'`

При `DEBUG = True` медиа-файлы раздаются через Django.

## Code Style

```bash
black .
isort .
flake8 .
```
