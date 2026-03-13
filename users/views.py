import secrets

from django.core.mail import send_mail
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.forms import UserRegisterForm
from users.models import User


# CRUD User
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'  # type: ignore
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'  # type: ignore
    context_object_name = 'user'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'  # type: ignore
    success_url = reverse_lazy('sending_messages:recipients_list')


class UserDeleteView(DeleteView):
    pass
