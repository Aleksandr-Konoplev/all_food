# Текущие URL контроллеров

Ниже перечислены все маршруты, подключенные в проекте на текущий момент.

| URL | Контроллер / view | Назначение |
| --- | --- | --- |
| `admin/` | `admin.site.urls` | Вход в административную панель Django |
| `users/login/` | `LoginView` | Авторизация пользователя |
| `users/logout/` | `LogoutView` | Выход пользователя из системы |
| `users/register/` | `UserCreateView` | Регистрация нового пользователя |
| `users/list/` | `UserListView` | Просмотр списка пользователей |
| `users/user/<int:pk>/detail/` | `UserDetailView` | Просмотр детальной информации о пользователе |
| `users/user/<int:pk>/update/` | `UserUpdateView` | Редактирование данных пользователя |

## Не подключено в маршруты

В коде также присутствует `UserDeleteView` в `users/views.py`, но на текущий момент для него не добавлен URL в `users/urls.py`.
