# Generated by Django 4.2.4 on 2023-08-28 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_blog'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='BlogPost',
        ),
    ]
