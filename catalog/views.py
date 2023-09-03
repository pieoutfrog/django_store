from django.contrib.admin import TabularInline
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contact, Category, BlogPost, MailingSettings, EmailLog
from catalog.forms import CreateProductForm, BlogPostForm


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


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogposts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'catalog/create_blog_post.html'
    form_class = BlogPostForm

    def form_valid(self, form):
        form.instance.is_published = True
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:blogpost_list')


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_details.html'
    context_object_name = 'blogposts'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'catalog/create_blog_post.html'
    form_class = BlogPostForm

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blogpost_view', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost

    def get_success_url(self):
        return reverse_lazy('catalog:blogpost_list')


# class MailingSettingsListView(View):
#     def get(self, request):
#         mailing_settings = MailingSettings.objects.all()
#         return render(request, 'catalog/mailing_settings_list.html', {'mailing_settings': mailing_settings})


# class MailingSettingsCreateView(CreateView):
#     template_name = 'catalog/mailing_settings_create.html'
#     model = MailingSettings
#
#     def form_valid(self, form):
#         mailing_settings = form.save(commit=False)
#         mailing_settings.start_time = timezone.now()
#         mailing_settings.end_time = timezone.now()
#         mailing_settings.save()
#
#         mailing_message = mailing_settings.mailing_message
#
#         email_log = EmailLog.objects.create(
#             status=form.cleaned_data['status'],
#             mailing_settings=mailing_settings
#         )
#
#         send_mail(
#             subject=mailing_message.subject,
#             message=mailing_message.message_content,
#             from_email='despero45@gmail.com',
#             recipient_list=[form.cleaned_data['email']],
#             fail_silently=False,
#         )
#
#         return redirect('catalog:mailing_settings_list')
#
#
# class MailingSettingsUpdateView(View):
#     def get(self, request, pk):
#         settings = MailingSettings.objects.get(pk=pk)
#         return render(request, 'catalog/mailing_settings_update.html', {'settings': settings})
#
#     def post(self, request, pk):
#         settings = MailingSettings.objects.get(pk=pk)
#         settings.start_time = request.POST.get('start_time')
#         settings.frequency = request.POST.get('frequency')
#         settings.status = request.POST.get('status')
#         settings.save()
#
#         return redirect('catalog:mailing_settings_list')
#
#
# class MailingSettingsDeleteView(View):
#     def post(self, pk):
#         settings = MailingSettings.objects.get(pk=pk)
#         settings.delete()
#
#         return redirect('catalog/mailing_settings_list')
