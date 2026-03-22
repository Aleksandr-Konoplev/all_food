from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from core.forms import ContentForSiteForm
from core.mixins import AddBaseContentMixin
from core.models import ContentForSite
from table_reservation.models import Reservation, Table
from users.mixins import ModeratorRequiredMixin
from users.models import User


class HomePageView(AddBaseContentMixin, TemplateView):
    template_name = 'core/home.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        context['address'] = ContentForSite.objects.get(name_content='address')
        context['phone'] = ContentForSite.objects.get(name_content='phone')
        context['working_hours'] = ContentForSite.objects.get(name_content='working_hours')
        context['restaurant_description'] = ContentForSite.objects.get(name_content='restaurant_description')
        return context


class AboutPageView(AddBaseContentMixin, TemplateView):
    template_name = 'core/about.html'  # noqa


class ControlPanelView(ModeratorRequiredMixin, AddBaseContentMixin, TemplateView):
    template_name = 'core/control_panel.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_items = ContentForSite.objects.order_by('name_content')

        context['stats_cards'] = [
            {'title': 'Контентных блоков', 'value': content_items.count(), 'description': 'Записи для текстов и изображений сайта.'},
            {'title': 'Пользователей', 'value': User.objects.count(), 'description': 'Все зарегистрированные аккаунты.'},
            {'title': 'Столиков', 'value': Table.objects.count(), 'description': 'Доступные столики для бронирования.'},
            {'title': 'Бронирований', 'value': Reservation.objects.count(), 'description': 'Все созданные бронирования.'},
        ]
        context['content_items'] = content_items
        context['quick_links'] = [
            {'label': 'Админка Django', 'href': '/admin/'},
            {'label': 'Тестовая страница', 'url_name': 'core:test-page'},
            {'label': 'Список бронирований', 'url_name': 'table_reservation:reservation-list'},
            {'label': 'Список пользователей', 'url_name': 'users:users-list'},
        ]
        return context


class ContentUpdateView(ModeratorRequiredMixin, UpdateView):
    model = ContentForSite
    form_class = ContentForSiteForm
    template_name = 'core/content_update.html'  # noqa

    def get_success_url(self):
        return reverse('core:content-update', kwargs={'pk': self.object.pk})


class TestPageView(AddBaseContentMixin, TemplateView):
    template_name = 'core/test_page.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        reservation = Reservation.objects.order_by('pk').first()  # type: ignore

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
