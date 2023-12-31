# Generated by Django 4.2.4 on 2023-10-09 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_remove_emaillog_server_response_mailingclient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingclient',
            options={'verbose_name': 'Клиент рассылки', 'verbose_name_plural': 'Клиенты рассылки'},
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.client', verbose_name='Клиент рассылки'),
        ),
    ]
