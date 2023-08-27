from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product, Contact, Category
from catalog.templates.catalog.forms import ProductForm


def home(request):
    latest_products = Product.objects.order_by('-id')[:5]
    context = {'latest_products': latest_products,
               'title': 'Наши последние товары'}
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        print(f'Имя пользователя: {name}, Почта: {email}, Сообщение: {message}')

    all_contacts = Contact.objects.all()
    context = {'all_contacts': all_contacts,
               'title': 'Контактные данные'}
    return render(request, 'catalog/contacts.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_details.html', context)


def products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 5)
    page = request.GET.get('page')
    try:
        product_page = paginator.page(page)
    except PageNotAnInteger:
        # Если номер страницы не является целым числом, отображаем первую страницу
        product_page = paginator.page(1)
    context = {'products': product_page}
    return render(request, 'catalog/products.html', context)


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category_products_list = Product.objects.filter(category=category)
    context = {'category': category, 'category_products_list': category_products_list}
    return render(request, 'catalog/category_products.html', context)



def create_product(request):
    error = ''
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            error = 'Неверная форма'

    form = ProductForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'catalog/product_create.html', context)
