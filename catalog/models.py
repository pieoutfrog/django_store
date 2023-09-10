from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='previews/', verbose_name='Превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    creation_date = models.DateField(verbose_name='Дата создания')
    last_change_date = models.DateField(verbose_name='Дата последнего изменения')
    active_version = models.OneToOneField('Version', related_name='+', **NULLABLE, on_delete=models.SET_NULL)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now().date()
        self.last_change_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}: {self.price} {self.description}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.CharField(max_length=100, verbose_name='Почта')
    message = models.TextField(verbose_name='Текст', **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.name}: {self.email}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class BlogPost(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.CharField(max_length=300, verbose_name='Slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Превью', **NULLABLE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}: {self.content}'

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
        ordering = ['-created_date']


class MailingMessage(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема')
    message_content = models.TextField(verbose_name='Содержание')
    objects = models.Manager()

    def __str__(self):
        return f'{self.subject}:\n {self.message_content}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Client(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=100, verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.full_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):
    objects = models.Manager()
    DELIVERY_FREQUENCY_CHOICES = (
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная'),
    )
    DELIVERY_STATUS_CHOICES = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('running', 'Запущена'),
    )
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)
    frequency = models.CharField(max_length=20, choices=DELIVERY_FREQUENCY_CHOICES, default='weekly')
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='created')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE,
                                verbose_name='Сообщение для рассылки', **NULLABLE)

    def __str__(self):
        return f"{self.frequency} рассылка в {self.start_time}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE,
                                verbose_name='Сообщение для рассылки', **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.client} / {self.settings}'

    class Meta:
        verbose_name = 'Клиент рассылки'


class EmailLog(models.Model):
    STATUSES = (
        ('STATUS_OK', 'Успешно'),
        ('STATUS_FAILED', 'Ошибка'),
    )
    datetime_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Последняя попытка')
    status = models.CharField(choices=STATUSES, default='STATUS_OK', verbose_name='Статус')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', **NULLABLE)
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки', **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'Логи рассылки - {self.datetime_attempt}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    version_number = models.CharField(max_length=50, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Текущая версия')
    objects = models.Manager()

    def __str__(self):
        return f"{self.product} - {self.version_number}"
