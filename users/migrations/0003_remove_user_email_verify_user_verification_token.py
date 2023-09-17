# Generated by Django 4.2.4 on 2023-09-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_email_verify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_verify',
        ),
        migrations.AddField(
            model_name='user',
            name='verification_token',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Код верификации'),
        ),
    ]
