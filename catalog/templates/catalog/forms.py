from catalog.models import Product, Category
from django.forms import ModelForm, TextInput, Textarea, Select
from django import forms
from datetime import datetime


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']