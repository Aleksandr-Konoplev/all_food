from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.http import HttpResponseRedirect

from django.urls import reverse, reverse_lazy

from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.forms import (
    ResendConfirmationForm,
    StyledPasswordResetForm,
    StyledSetPasswordForm,
    UserLoginForm,
    UserRegisterForm,
    UserUpdateForm,
)
from users.mixins import UserAccessQuerysetMixin, ModeratorRequiredMixin
from users.models import User
from users.services import resend_activation_email, send_activation_email
from core.mixins import AddBaseContentMixin


# CRUD User
class UserCreateView(AddBaseContentMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save(update_fields=['is_active'])
        send_activation_email(user, self.request, regenerate_token=True)
        messages.success(
            self.request,
            'Аккаунт создан. Мы отправили письмо для подтверждения email. Если письмо потеряется, его можно отправить повторно.',
        )
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


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


class UserLoginView(AddBaseContentMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'  # type: ignore
    success_url = reverse_lazy('core:home')


class UserLogoutView(AddBaseContentMixin, LogoutView):
    success_url = reverse_lazy('users:login')


class ResendConfirmationView(AddBaseContentMixin, FormView):
    template_name = 'users/resend_confirmation.html'
    form_class = ResendConfirmationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        resend_activation_email(form.cleaned_data['email'], self.request)
        messages.success(
            self.request,
            'Если для этого email требуется подтверждение, новое письмо уже отправлено.',
        )
        return super().form_valid(form)


class UserPasswordResetView(AddBaseContentMixin, PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = StyledPasswordResetForm
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password-reset-done')


class UserPasswordResetDoneView(AddBaseContentMixin, PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(AddBaseContentMixin, PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy('users:password-reset-complete')


class UserPasswordResetCompleteView(AddBaseContentMixin, PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
