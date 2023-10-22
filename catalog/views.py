from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contact, Category, BlogPost, MailingClient, Version, Client, MailingSettings, \
    EmailLog
from catalog.forms import CreateProductForm, BlogPostForm, VersionForm, MailingSettingsCreateForm


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


class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'catalog/product_create.html'
    extra_context = {'error': ''}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))

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


class MailingSettingsListView(ListView):
    model = MailingClient
    template_name = 'catalog/mailing_list.html'
    context_object_name = 'mailing_clients'


class MailingSettingsCreateView(CreateView):
    template_name = 'catalog/mailing_settings_create.html'
    model = MailingClient
    form_class = MailingSettingsCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']  # Получаем объект MailingMessage из формы
        mailing_settings = MailingSettings.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now(),
            status=form.cleaned_data['status'] or None,
            message=mailing_message,  # Присваиваем объект MailingMessage
        )

        MailingClient.objects.create(
            client=form.cleaned_data['client'],
            settings=mailing_settings,
            message=mailing_message,  # Присваиваем объект MailingMessage
        )

        email_log = EmailLog.objects.create(
            client=form.cleaned_data['client'],
            status=form.cleaned_data['status'],
            settings=mailing_settings,
        )

        email_log.message = mailing_message  # Присваиваем объект MailingMessage
        email_log.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:mailing_list')


class MailingSettingsDetailView(DetailView):
    template_name = 'catalog/mailing_details.html'
    model = MailingSettings
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнительный код для получения дополнительных данных, если требуется
        return context


class MailingSettingsUpdateView(UpdateView):
    template_name = 'catalog/mailing_settings_create.html'
    model = MailingSettings
    form_class = MailingSettingsCreateForm

    def form_valid(self, form):
        mailing_message = form.cleaned_data['message']
        mailing_settings = form.save(commit=False)
        mailing_settings.message = mailing_message
        mailing_settings.save()

        mailing_client = MailingClient.objects.get(settings_id=mailing_settings.id)
        mailing_client.client = form.cleaned_data['client']
        mailing_client.message = mailing_message
        mailing_client.save()

        email_log = EmailLog.objects.get(settings=mailing_settings)
        email_log.client = form.cleaned_data['client']
        email_log.status = form.cleaned_data['status']
        email_log.message = mailing_message
        email_log.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:mailing_details', args=[self.kwargs.get('pk')])


class MailingSettingsDeleteView(DeleteView):
    template_name = 'catalog/mailingclient_confirm_delete.html'
    model = MailingSettings

    def get_success_url(self):
        return reverse_lazy('catalog:mailing_list')


class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/create_version.html'
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        # if form.instance.author != self.request.user:
        #     redirect('users/error_create')
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)

        version = form.save(commit=False)
        version.product = product

        if version.is_current:
            active_version = Version.objects.filter(product=product, is_current=True).first()
            if active_version:
                active_version.is_current = False
                active_version.save()

            product.active_version = version
            product.save()

        return super().form_valid(form)
