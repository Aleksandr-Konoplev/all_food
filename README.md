# All Food

Веб-приложение на Django для сайта ресторана: публичные страницы, регистрация пользователей, подтверждение email и бронирование столиков.

## Что есть в проекте

- `core` - главная страница, страница "О ресторане", обратная связь, контент сайта, панель управления
- `users` - кастомная модель пользователя, авторизация по email, регистрация и подтверждение почты
- `table_reservation` - столики и CRUD бронирований с проверкой пересечений по времени
- роли: пользователь, модератор, суперпользователь
- email через две SMTP-конфигурации: `main` и `auto`

## Стек

- Python `>=3.14`
- Django `>=6.0.3`
- PostgreSQL
- Pillow
- python-dotenv
- psycopg2
- black, isort, flake8

Зависимости описаны в `pyproject.toml`.

## Структура проекта

- `config` - настройки Django, маршруты, ASGI/WSGI
- `core` - страницы сайта, блоки контента, обратная связь, management-команды
- `users` - пользователи, регистрация, подтверждение email, профили
- `table_reservation` - столики, бронирования, проверка доступности
- `static` - статика проекта
- `media` - загружаемые файлы

## Переменные окружения

Проект использует `.env` и ожидает:

```env
SECRET_KEY=

NAME=
USER=
PASSWORD=
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
```

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install -e .
python manage.py migrate
python manage.py loaddata core/fixtures/default_content_for_site.json
python manage.py loaddata core/fixtures/default_groups.json
python manage.py loaddata core/fixtures/default_table.json
python manage.py custom_csu
python manage.py runserver
```

## Основные сущности

- `users.User` - пользователь с логином по `email`, без `username`
- `core.ContentForSite` - редактируемые блоки текста и изображений
- `core.Feedback` - сообщения из формы обратной связи
- `table_reservation.Table` - столик, количество мест, описание, минимальный депозит
- `table_reservation.Reservation` - бронирование столика на интервал времени

## Особенности логики

- новый пользователь создается неактивным и активируется по ссылке из email
- для модератора используется группа `moderator`
- депозит бронирования автоматически берется из `Table.min_deposit`
- нельзя создать пересекающиеся бронирования для одного столика
- на странице бронирования показывается занятость столов по выбранному дню

## Фикстуры

В проекте есть стартовые фикстуры:

- `core/fixtures/default_content_for_site.json`
- `core/fixtures/default_groups.json`
- `core/fixtures/default_table.json`

Загрузка:

```bash
python manage.py loaddata core/fixtures/default_content_for_site.json
python manage.py loaddata core/fixtures/default_groups.json
python manage.py loaddata core/fixtures/default_table.json
```

Если фикстура лежит в папке `fixtures`, можно использовать короткий вариант, например:

```bash
python manage.py loaddata default_groups
```

## Management-команды

- `python manage.py custom_csu` - создать суперпользователя для кастомной модели
- `python manage.py dumpfixture core.ContentForSite core/fixtures/content_for_site.json` - выгрузить данные модели в JSON
- `python manage.py dumpfixture table_reservation.Table core/fixtures/tables.json` - выгрузить столики в JSON
- `python manage.py dumpdata auth.group --indent 2 > core/fixtures/groups.json` - выгрузить группы
- `python manage.py loaddata core/fixtures/groups.json` - загрузить группы
- `python manage.py full_reset_db` - полностью очистить PostgreSQL БД

## Маршруты

- `/` - главная страница
- `/about/` - страница о ресторане
- `/control-panel/` - панель управления модератора
- `/content/` - список блоков контента
- `/content/<int:pk>/update/` - редактирование блока контента
- `/feedbacks/` - список сообщений обратной связи
- `/users/login/`, `/users/logout/`, `/users/register/`
- `/users/email-confirm/<str:token>/` - подтверждение email
- `/users/list/` - список пользователей
- `/reserve/create/`, `/reserve/list/`
- `/reserve/<int:pk>/detail/`, `/reserve/<int:pk>/update/`, `/reserve/<int:pk>/delete/`

## Code Style

```bash
black .
isort .
flake8 .
```

## Что важно учесть

- проект настроен на PostgreSQL
- `AUTH_USER_MODEL` - `users.User`
- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `test-page/` используется для локальной проверки и не нужен в production
- тесты в приложениях пока почти не реализованы
