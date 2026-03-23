# All Food

Веб-приложение на Django для сайта ресторана: публичные страницы, регистрация пользователей, подтверждение email и бронирование столиков.

## Что есть в проекте

- `core` - главная страница, страница "О ресторане", тестовая страница, редактируемый контент сайта и панель управления
- `users` - кастомная модель пользователя с авторизацией по email, с подтверждением почты
- `table_reservation` - CRUD для бронирований, контроль пересечений по времени и привязка депозита к столику
- права доступа через обычного пользователя, модератора и суперпользователя
- отправка email через две SMTP-конфигурации: `main` и `auto`

## Стек

- Python `>=3.14`
- Django `>=6.0.3`
- PostgreSQL
- Pillow
- python-dotenv
- psycopg2

Зависимости описаны в `pyproject.toml`.

## Конфигурация проекта

Основные настройки находятся в `config/settings.py`.

- база данных - PostgreSQL
- кастомная модель пользователя - `users.User`
- `LOGIN_URL` - `users:login`
- `LOGIN_REDIRECT_URL` - `core:home`
- `LOGOUT_REDIRECT_URL` - `core:home`
- язык - `en-us`
- часовой пояс - `UTC`
- статика - `static/`
- медиа - `media/`

### Переменные окружения

Проект использует файл `.env` и ожидает следующие переменные:

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
python manage.py runserver
```

Если нужен суперпользователь для кастомной модели, используйте:

```bash
python manage.py custom_csu
```

## Сущности

### Пользователь

- логин по `email`
- `username` отключен
- поддерживаются `avatar`, `phone_number`, `tg_chat_id`
- после регистрации пользователь создается неактивным и активируется через ссылку из email

### Столик

- номер столика
- количество мест
- описание
- минимальный депозит

### Бронирование

- владелец бронирования
- время начала и окончания
- выбранный столик
- депозит, который автоматически синхронизируется с `min_deposit` столика
- валидация пересечений по времени для одного столика

## Роли и доступы

- обычный пользователь видит и редактирует только свои профиль и бронирования
- модератор и суперпользователь получают расширенный доступ к спискам и объектам
- `ControlPanelView` и список пользователей доступны только модератору или суперпользователю

Для модератора используется группа `moderator`.

## Полезные management-команды

- **Пользователь**
  - `python manage.py custom_csu` - Создание суперпользователя.
- **База данных**
  - *Сброс и восстановление схем*
    - `python manage.py full_reset_db` - **ВНИМАНИЕ!** Полная очистка базы данных. Перед выполнением убедитесь что вы
    сделали выгрузку данных (если они нужны) 
    - `python manage.py migrate` - Применить миграции
  - *Контент*
    - `python manage.py dumpdata core.ContentForSite --indent 4 --output core/fixtures/content_for_site.json` - 
    Сохранение столов в json-файл из БД. 
    - `python manage.py loaddata core/fixtures/default_content_for_site.json` - Загрузка блоков контента для наполнения 
    сайта в базу данных (измените имя json-файла для загрузки ранее сохранённой схемы столов)

  - *Столы*
    - `python manage.py dumpdata table_reservation.Table --indent 4 --output core/fixtures/tables.json` - 
    Сохранение столов в json-файл из БД.
    - `python manage.py loaddata core/fixtures/default_tables.json` - Загрузка схемы столов в базу данных (измените имя
    json-файла для загрузки ранее сохранённой схемы столов)


## Текущие маршруты

| URL | Контроллер / view | Назначение |
| --- | --- | --- |
| `/` | `HomePageView` | Главная страница сайта |
| `admin/` | `admin.site.urls` | Вход в административную панель Django |
| `about/` | `AboutPageView` | Страница с информацией о ресторане |
| `control-panel/` | `ControlPanelView` | Панель управления для модератора |
| `content/<int:pk>/update/` | `ContentUpdateView` | Редактирование контентного блока сайта |
| `test-page/` | `TestPageView` | Тестовая страница со ссылками на основные сущности |
| `users/login/` | `LoginView` | Авторизация пользователя |
| `users/logout/` | `LogoutView` | Выход пользователя из системы |
| `users/register/` | `UserCreateView` | Регистрация нового пользователя |
| `users/email-confirm/<str:token>/` | `email_verification` | Подтверждение email и активация аккаунта |
| `users/list/` | `UserListView` | Просмотр списка пользователей |
| `users/user/<int:pk>/detail/` | `UserDetailView` | Просмотр детальной информации о пользователе |
| `users/user/<int:pk>/update/` | `UserUpdateView` | Редактирование данных пользователя |
| `users/user/<int:pk>/delete/` | `UserDeleteView` | Удаление пользователя |
| `reserve/create/` | `ReservationCreateView` | Создание бронирования столика |
| `reserve/list/` | `ReservationListView` | Просмотр списка бронирований |
| `reserve/<int:pk>/detail/` | `ReservationDetailView` | Просмотр деталей бронирования |
| `reserve/<int:pk>/update/` | `ReservationUpdateView` | Редактирование бронирования |
| `reserve/<int:pk>/delete/` | `ReservationDeleteView` | Удаление бронирования |

## Что еще стоит учитывать

- тесты в приложениях пока не реализованы
- `DEBUG` сейчас включен
- `ALLOWED_HOSTS` пока пустой и требует настройки для deployment
