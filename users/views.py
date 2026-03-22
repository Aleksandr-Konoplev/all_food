import secrets

from core.services import custom_send_email
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm
from users.mixins import UserAccessQuerysetMixin, ModeratorRequiredMixin
from users.models import User
from core.mixins import AddBaseContentMixin


# CRUD User
class UserCreateView(AddBaseContentMixin, CreateView):
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
        url = f"https://{host}/users/email-confirm/{token}"
        custom_send_email('auto', 'Активация аккаунта', f'Перейдите по ссылке: {url} для регистрации аккаунта', [user.email])

        return super().form_valid(form)


class UserListView(AddBaseContentMixin, ModeratorRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'  # type: ignore
    context_object_name = 'users'


class UserDetailView(AddBaseContentMixin, UserAccessQuerysetMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'  # type: ignore
    context_object_name = 'user'


class UserUpdateView(AddBaseContentMixin, UserAccessQuerysetMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'  # type: ignore

    def get_success_url(self):
        return reverse_lazy('users:user-detail', kwargs={'pk': self.object.pk})


class UserDeleteView(AddBaseContentMixin, UserAccessQuerysetMixin, DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'  # type: ignore
    success_url = reverse_lazy('users:login')
