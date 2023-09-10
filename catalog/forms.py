from django.forms import DateTimeInput

from catalog.models import Product, BlogPost, MailingSettings
from django import forms


class CreateProductForm(forms.ModelForm):

    def form_invalid(self):
        self.error = 'Неверная форма'

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']


class BlogPostForm(forms.ModelForm):
    preview = forms.ImageField(label='Загрузить изображение')

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview']


class MailingSettingsForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


