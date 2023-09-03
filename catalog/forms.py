from catalog.models import Product, BlogPost
from django import forms


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']


class BlogPostForm(forms.ModelForm):
    preview = forms.ImageField(label='Загрузить изображение')

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview']


