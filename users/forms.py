from django.contrib.auth.forms import UserCreationForm
from users.models import User


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
        self.fields['phone_number'].help_text = 'Введите номер телефона в формате +7 ХХХ ХХ ХХ'
