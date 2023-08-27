from django.core.management import BaseCommand
from django.core.management import call_command
from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        # удаляю, как в shell
        Category.objects.all().delete()
        # вызываю фикстуру
        call_command('loaddata', 'data.json')
        # получаю все объекты из БД
        categories = Category.objects.all()
        categories_for_create = []
        for category in categories:
            # сбрасываю айди, чтобы не было конфликта
            category.id = None
            categories_for_create.append(category)
        Category.objects.bulk_create(categories_for_create)
        # использую exclude для исключения объектов Category, чьи pk (id) присутствуют в исходном списке categories
        Category.objects.exclude(pk__in=[category.pk for category in categories]).delete()
