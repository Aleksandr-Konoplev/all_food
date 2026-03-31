from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView, FormMixin

from core.forms import ContentForSiteForm, FeedbackForm
from core.mixins import AddBaseContentMixin
from core.models import ContentForSite, Feedback
from table_reservation.models import Reservation, Table
from users.mixins import ModeratorRequiredMixin
from users.models import User


class HomePageView(AddBaseContentMixin, FormMixin, TemplateView):
    template_name = 'core/home.html'  # noqa
    success_url = reverse_lazy('core:home')
    form_class = FeedbackForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        context['address'] = ContentForSite.objects.get(name_tag='address')
        context['phone'] = ContentForSite.objects.get(name_tag='phone')
        context['working_hours'] = ContentForSite.objects.get(name_tag='working_hours')
        context['restaurant_description'] = ContentForSite.objects.get(name_tag='restaurant_description')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.owner = request.user
            feedback.save()
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AboutPageView(AddBaseContentMixin, TemplateView):
    template_name = 'core/about.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history_restaurant'] = ContentForSite.objects.get(name_tag='history_restaurant')
        context['mission_and_values'] = ContentForSite.objects.get(name_tag='mission_and_values')
        context['people_chef_cook'] = ContentForSite.objects.get(name_tag='people_chef_cook')
        context['people_hall_team'] = ContentForSite.objects.get(name_tag='people_hall_team')
        context['people_admin'] = ContentForSite.objects.get(name_tag='people_admin')
        context['description_team'] = ContentForSite.objects.get(name_tag='description_team')
        return context


class ControlPanelView(ModeratorRequiredMixin, AddBaseContentMixin, TemplateView):
    template_name = 'core/control_panel.html'  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        count_feedback = Feedback.objects.count()
        active_reservations_count = Reservation.objects.filter(end_at__gt=timezone.now()).count()

        context['stats_cards'] = [
            {'title': 'Сообщения клиентов', 'value': count_feedback, 'description': 'Сообщения от клиентов присланные через форму.'},
            {'title': 'Пользователей', 'value': User.objects.count(), 'description': 'Все зарегистрированные аккаунты.'},
            {'title': 'Столиков', 'value': Table.objects.count(), 'description': 'Доступные столики для бронирования.'},
            {'title': 'Бронирований', 'value': active_reservations_count, 'description': 'Бронирования, у которых время окончания еще не наступило.'},
        ]
        context['quick_links'] = [
            {'label': 'Админка Django', 'href': '/admin/'},
            {'label': 'Контент сайта', 'url_name': 'core:content-list'},
            {'label': 'Сообщения обратной связи', 'url_name': 'core:feedbacks-list'},
            {'label': 'Тестовая страница', 'url_name': 'core:test-page'},
            {'label': 'Список бронирований', 'url_name': 'table_reservation:reservation-list'},
            {'label': 'Список пользователей', 'url_name': 'users:users-list'},
        ]
        return context


class ContentListView(ModeratorRequiredMixin, ListView):
    model = ContentForSite
    template_name = 'core/content_list.html'  # noqa
    context_object_name = 'content_items'

    def get_queryset(self):
        return ContentForSite.objects.order_by('name_tag')


class ContentUpdateView(ModeratorRequiredMixin, UpdateView):
    model = ContentForSite
    form_class = ContentForSiteForm
    template_name = 'core/content_update.html'  # noqa

    def get_success_url(self):
        return reverse('core:content-update', kwargs={'pk': self.object.pk})


# Отзывы
class FeedbackListView(ModeratorRequiredMixin, ListView):
    model = Feedback
    template_name = 'core/feedbacks_list.html'  # noqa
    context_object_name = 'feedbacks'


class FeedbackDetailView(ModeratorRequiredMixin, DetailView):
    model = Feedback
    template_name = 'core/feedback_detail.html'  # noqa
    context_object_name = 'feedback'


class FeedbackDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'core/confirm_delete_feedback.html'  # noqa
    success_url = reverse_lazy('core:feedbacks-list')


# Страница для тестирования эндпоинтов. Удалить перед деплоем!
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
