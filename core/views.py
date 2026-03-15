from django.views.generic import TemplateView

from core.mixins import AddTextContentMixin
from table_reservation.models import Reservation


class HomePageView(AddTextContentMixin, TemplateView):
    template_name = 'core/home.html'  # noqa


class AboutPageView(AddTextContentMixin, TemplateView):
    template_name = 'core/about.html'  # noqa


class TestPageView(AddTextContentMixin, TemplateView):
    template_name = 'core/test_page.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        reservation = Reservation.objects.order_by('pk').first()  # type: ignore[attr-defined]

        user_pk = user.pk if user.is_authenticated else None
        reservation_pk = reservation.pk if reservation else None

        context['entity_links'] = [
            {
                'title': 'Core',
                'links': [
                    {'label': 'Главная', 'url_name': 'core:home'},
                    {'label': 'О ресторане', 'url_name': 'core:about'},
                    {'label': 'Тестовая страница', 'url_name': 'core:test-page'},
                ],
            },
            {
                'title': 'User',
                'links': [
                    {'label': 'Вход', 'url_name': 'users:login'},
                    {'label': 'Выход', 'url_name': 'users:logout'},
                    {'label': 'Регистрация', 'url_name': 'users:register'},
                    {'label': 'Список пользователей', 'url_name': 'users:users-list'},
                    {'label': 'Профиль пользователя', 'url_name': 'users:user-detail', 'pk': user_pk, 'empty_text': 'требуется авторизация'},
                    {'label': 'Редактирование пользователя', 'url_name': 'users:user-update', 'pk': user_pk, 'empty_text': 'требуется авторизация'},
                    {'label': 'Удаление пользователя', 'url_name': 'users:user-delete', 'pk': user_pk, 'empty_text': 'требуется авторизация'},
                ],
            },
            {
                'title': 'Reservation',
                'links': [
                    {'label': 'Создать бронирование', 'url_name': 'table_reservation:reservation-create'},
                    {'label': 'Список бронирований', 'url_name': 'table_reservation:reservation-list'},
                    {'label': 'Детали бронирования', 'url_name': 'table_reservation:reservation-detail', 'pk': reservation_pk, 'empty_text': 'в базе нет бронирований'},
                    {'label': 'Редактирование бронирования', 'url_name': 'table_reservation:reservation-update', 'pk': reservation_pk, 'empty_text': 'в базе нет бронирований'},
                    {'label': 'Удаление бронирования', 'url_name': 'table_reservation:reservation-delete', 'pk': reservation_pk, 'empty_text': 'в базе нет бронирований'},
                ],
            },
            {
                'title': 'Admin',
                'links': [
                    {'label': 'Админка', 'href': '/admin/'},
                ],
            },
        ]
        return context
