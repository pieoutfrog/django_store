from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product

# # Получаем content type для модели Product
# content_type = ContentType.objects.get_for_model(Product)
#
# # Создаем разрешения
# Permission.objects.create(
#     codename='can_set_product_publication',
#     name='Can set product publication',
#     content_type=content_type,
# )
# Permission.objects.create(
#     codename='can_change_product_description',
#     name='Can change product description',
#     content_type=content_type,
# )
# Permission.objects.create(
#     codename='can_change_product_category',
#     name='Can change product category',
#     content_type=content_type,
# )
