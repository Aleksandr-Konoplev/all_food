from django import forms

from core.models import ContentForSite


class ContentForSiteForm(forms.ModelForm):
    class Meta:
        model = ContentForSite
        fields = ('name_tag', 'text', 'image')
        labels = {
            'name_tag': 'Ключ контента',
            'text': 'Текст',
            'image': 'Изображение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_tag'].widget.attrs.update(
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
