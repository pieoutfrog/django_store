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
    price = models.DecimalField(max_digits=8, decimal_places=2)
    creation_date = models.DateField(verbose_name='Дата создания')
    last_change_date = models.DateField(verbose_name='Дата последнего изменения')
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
