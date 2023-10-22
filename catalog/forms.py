from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from catalog.models import Product, BlogPost, MailingClient, Version, Client, MailingMessage, MailingSettings
from django import forms


class CreateProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('создать', 'Создать'))

    def form_invalid(self):
        self.error = 'Неверная форма'

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError("Название содержит запрещенное слово.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError("Описание содержит запрещенное слово.")
        return description

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('user',)


class BlogPostForm(forms.ModelForm):
    preview = forms.ImageField(label='Загрузить изображение')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview']

    # start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    # end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class MailingSettingsCreateForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
        }

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')
        product = cleaned_data.get('product')

        if is_current and Version.objects.filter(product=product, is_current=True).count() > 1:
            raise forms.ValidationError('Может быть только одна текущая версия для данного продукта.')

        return cleaned_data

    def clean_is_current(self):
        is_current = self.cleaned_data.get('is_current')
        if is_current is None:
            is_current = False
        return is_current
