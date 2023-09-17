from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.ru',
            first_name='Alisa',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123456789')
        user.save()
