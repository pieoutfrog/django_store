# Generated by Django 4.2.4 on 2023-11-03 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_product_is_published_alter_emaillog_client_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_set_product_publication', 'Can set product publication'), ('can_change_product_description', 'Can change product description'), ('can_change_product_category', 'Can change product category')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
