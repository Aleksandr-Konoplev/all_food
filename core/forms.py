from django import forms

from core.models import ContentForSite, Feedback


class ContentForSiteForm(forms.ModelForm):
    class Meta:
        model = ContentForSite
        fields = ("name_tag", "text", "image")
        labels = {
            "name_tag": "Ключ контента",
            "text": "Текст",
            "image": "Изображение",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name_tag"].widget.attrs.update({"class": "form-control", "placeholder": "Например, greeting"})
        self.fields["text"].widget = forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Введите текст для этого блока сайта",
            }
        )
        self.fields["image"].widget.attrs.update({"class": "form-control"})


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("user_name", "phone", "email", "body")
        labels = {
            "user_name": "Имя",
            "phone": "Телефон",
            "email": "Email",
            "body": "Сообщение",
        }
        widgets = {
            "user_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, Анна"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 (900) 000-00-00"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.ru"}),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Напишите ваш вопрос или пожелание",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields["user_name"].initial = user.first_name
            self.fields["phone"].initial = user.phone_number
            self.fields["email"].initial = user.email
