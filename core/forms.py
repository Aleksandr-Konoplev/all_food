from django import forms

from core.models import ContentForSite


class ContentForSiteForm(forms.ModelForm):
    class Meta:
        model = ContentForSite
        fields = ('name_content', 'text', 'image')
        labels = {
            'name_content': 'Ключ контента',
            'text': 'Текст',
            'image': 'Изображение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_content'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Например, greeting'}
        )
        self.fields['text'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Введите текст для этого блока сайта',
            }
        )
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
