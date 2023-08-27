from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product, Contact, Category
from catalog.templates.catalog.forms import CreateProductForm


class HomeView(ListView):
    model = Product
    queryset = Product.objects.order_by('-id')[:5]
    template_name = 'catalog/home.html'
    context_object_name = 'latest_products'
    extra_context = {'title': 'Наши последние товары'}


class ContactsView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'
    context_object_name = 'all_contacts'
    extra_context = {'title': 'Контактные данные'}

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        print(f'Имя пользователя: {name}, Почта: {email}, Сообщение: {message}')
        return redirect('contacts')


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'catalog/product_details.html'
    context_object_name = 'product'


class ProductsView(ListView):
    model = Product
    template_name = 'catalog/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение всех объектов модели Product
        products = Product.objects.all()

        # Создание экземпляра класса Paginator
        paginator = Paginator(products, 5)  # Здесь 10 - количество объектов на странице

        # Получение номера запрошенной страницы из параметра запроса
        page_number = self.request.GET.get('page')

        try:
            # Получение объектов для указанной страницы
            page_objects = paginator.get_page(page_number)
        except EmptyPage:
            # Если номер страницы недопустим, возвращаем последнюю страницу
            page_objects = paginator.get_page(paginator.num_pages)

        # Добавление объектов в контекст шаблона
        context['products'] = page_objects

        return context


class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'category_products_list'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        queryset = Product.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        return context


class CreateProductView(CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'catalog/product_create.html'
    extra_context = {'error': ''}

    def form_invalid(self, form):
        self.extra_context['error'] = 'Неверная форма'
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('catalog:products')
