from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.forms import ModelForm
from users.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Email'
        self.fields['username'].help_text = 'Используйте email, указанный при регистрации'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'example@mail.ru',
            'autocomplete': 'email',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Введите пароль',
            'autocomplete': 'current-password',
        })


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'avatar',
            'phone_number',
            'first_name',
            'last_name',
        )
        labels = {
            'email': 'Email',
            'avatar': 'Аватар',
            'phone_number': 'Номер телефона',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        self.fields['password1'].help_text = 'Минимум 8 символов, не простой пароль.'
        self.fields['password2'].help_text = 'Введите тот же пароль ещё раз.'
        self.fields['email'].help_text = 'Введите вашу электронную почту'
        self.fields['phone_number'].help_text = 'Введите номер телефона в формате +7 ХХХ ХХ ХХ'
        self.fields['first_name'].help_text = 'Введите ваше имя'
        self.fields['last_name'].help_text = 'Введите вашу фамилию'

        self.fields['email'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'example@mail.ru',
            'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Придумайте пароль',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password',
        })
        self.fields['avatar'].widget.attrs.update({'class': 'form-control auth-input'})
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': '+7 (900) 000-00-00',
            'autocomplete': 'tel',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Ваше имя',
            'autocomplete': 'given-name',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Ваша фамилия',
            'autocomplete': 'family-name',
        })


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'avatar',
            'phone_number',
            'first_name',
            'last_name',
        )
        labels = {
            'email': 'Email',
            'avatar': 'Аватар',
            'phone_number': 'Номер телефона',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].help_text = 'Введите вашу электронную почту'
        self.fields['phone_number'].help_text = 'Введите номер телефона в формате +7 ХХХ ХХ ХХ'
        self.fields['first_name'].help_text = 'Введите ваше имя'
        self.fields['last_name'].help_text = 'Введите вашу фамилию'

        self.fields['email'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'example@mail.ru',
            'autocomplete': 'email',
        })
        self.fields['avatar'].widget.attrs.update({'class': 'form-control auth-input'})
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': '+7 (900) 000-00-00',
            'autocomplete': 'tel',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Ваше имя',
            'autocomplete': 'given-name',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Ваша фамилия',
            'autocomplete': 'family-name',
        })


class ResendConfirmationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        help_text='Введите email, указанный при регистрации',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control auth-input',
                'placeholder': 'example@mail.ru',
                'autocomplete': 'email',
            }
        ),
    )


class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = 'Мы отправим ссылку для сброса пароля на эту почту'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'example@mail.ru',
            'autocomplete': 'email',
        })


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение пароля'

        self.fields['new_password1'].help_text = 'Минимум 8 символов, не простой пароль.'
        self.fields['new_password2'].help_text = 'Введите тот же пароль ещё раз.'

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Придумайте новый пароль',
            'autocomplete': 'new-password',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Повторите новый пароль',
            'autocomplete': 'new-password',
        })
