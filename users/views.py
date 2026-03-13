import secrets

from django.core.mail import send_mail
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm
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
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'  # type: ignore

    def get_success_url(self):
        return reverse_lazy('users:user-detail', kwargs={'pk': self.object.pk})


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'  # type: ignore
    success_url = reverse_lazy('users:login')
