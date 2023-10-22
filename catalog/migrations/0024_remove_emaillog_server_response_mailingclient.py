# Generated by Django 4.2.4 on 2023-10-04 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_emaillog_server_response_delete_mailingclient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='server_response',
        ),
        migrations.CreateModel(
            name='MailingClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.client', verbose_name='Клиент')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.mailingmessage', verbose_name='Сообщение для рассылки')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.mailingsettings', verbose_name='Настройки')),
            ],
            options={
                'verbose_name': 'Клиент рассылки',
            },
        ),
    ]