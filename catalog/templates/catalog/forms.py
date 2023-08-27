from catalog.models import Product, Category
from django.forms import ModelForm, TextInput, Textarea, Select
from django import forms
from datetime import datetime


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
# class ProductForm(ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')
#     last_change_date = forms.DateTimeField(initial=datetime.now,
#                                            widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
#     creation_date = forms.DateTimeField(initial=datetime.now,
#                                         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
#
#     class Meta:
#         model = Product
#         fields = ['name', 'price', 'description', 'category', 'creation_date', 'last_change_date']
#         widgets = {
#             'name': TextInput(attrs={'class': 'form-group'}),
#             'price': TextInput(attrs={'class': 'form-group'}),
#             'description': Textarea(attrs={'class': 'form-group'}),
#             'category': Select(attrs={'class': 'form-group'}),
#             'creation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'last_change_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }
#         labels = {
#             'name': 'Название',
#             'price': 'Цена',
#             'description': 'Описание',
#         }
