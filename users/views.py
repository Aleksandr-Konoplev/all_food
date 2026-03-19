import secrets

from core.services import custom_send_email
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm
from users.mixins import UserAccessQuerysetMixin, ModeratorRequiredMixin
from users.models import User


# CRUD User
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        custom_send_email('auto', 'Активация аккаунта', f'Перейдите по ссылке: {url} для регистрации аккаунта', [user.email])

        return super().form_valid(form)


class UserListView(ModeratorRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'  # type: ignore
    context_object_name = 'users'


class UserDetailView(UserAccessQuerysetMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'  # type: ignore
    context_object_name = 'user'


class UserUpdateView(UserAccessQuerysetMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'  # type: ignore

    def get_success_url(self):
        return reverse_lazy('users:user-detail', kwargs={'pk': self.object.pk})


class UserDeleteView(UserAccessQuerysetMixin, DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'  # type: ignore
    success_url = reverse_lazy('users:login')
