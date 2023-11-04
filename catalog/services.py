from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import Category
from .models import MailingSettings


def add_jobs(scheduler):
    for mailing_setting in MailingSettings.objects.filter(status='running'):
        add_job(scheduler, mailing_setting)


def add_job(scheduler, mailing_setting):
    # задать вопрос про интервал и как использовать уже имеющиеся настройки рассылки в часах, днях и т.д.
    for mailing_setting in MailingSettings.objects.filter(status='running'):
        hours, minutes = mailing_setting.start_time.hour, mailing_setting.start_time.minute
        if mailing_setting.frequency == 'daily':
            trigger_time = CronTrigger(day="*", hour=hours, minute=minutes)
            scheduler.add_job(
                sending_mail,
                trigger=trigger_time,
                id=str(mailing_setting.pk),
                max_instances=1,
                replace_existing=True,
                args=(mailing_setting,)
            )
        elif mailing_setting.frequency == 'weekly':
            trigger_time = CronTrigger(day_of_week='mon', hour=hours, minute=minutes)
            scheduler.add_job(
                sending_mail,
                trigger=trigger_time,
                id=str(mailing_setting.pk),
                max_instances=1,
                replace_existing=True,
                args=(mailing_setting,)
            )
        elif mailing_setting.frequency == 'monthly':
            trigger_time = CronTrigger(day='1', hour=hours, minute=minutes)
            scheduler.add_job(
                sending_mail,
                trigger=trigger_time,
                id=str(mailing_setting.pk),
                max_instances=1,
                replace_existing=True,
                args=(mailing_setting,)
            )


def sending_mail(mailing_setting):
    clients = mailing_setting.client.all()
    email_list = [client.email for client in clients]
    message = mailing_setting.message
    send_mail(
        subject=message.subject,
        message=message.message_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
        fail_silently=False,
    )


def get_categories():
    # Пытаемся получить категории из кеша
    categories = cache.get('categories')

    if categories is None:
        # Если категории не найдены в кеше, делаем выборку из базы данных
        categories = Category.objects.all()

        # Сохраняем результаты в кеше на определенный период времени
        cache.set('categories', categories, 60 * 15)

    return categories
