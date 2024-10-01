from celery import shared_task
from django.core.mail import EmailMultiAlternatives
import datetime
from django.template.loader import render_to_string

from AnnouncementBoard.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .models import Announcement, Category, Response


@shared_task()
def announcement_created_notification(pk):
    announcement = Announcement.objects.get(pk=pk)
    title = 'Новое объявление'
    category = announcement.category
    emails = []
    subscribers = category.subscribers.all()
    for subscriber in subscribers:
        emails.append(subscriber.email)
    html_context = render_to_string(
        'email/announcement_created_letter.html',
        {
            'link': f'{SITE_URL}/{pk}',
            'title': announcement.title,
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=emails,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task()
def response_created_notification(pk):
    response = Response.objects.get(pk=pk)
    title = 'Отклик на ваше объявление'
    email = [response.receiver.email]
    html_context = render_to_string(
        'email/response_created_letter.html',
        {
            'link': f'{SITE_URL}/{response.announcement.pk}',
            'text': response.text,
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task()
def response_accepted_notification(pk):
    response = Response.objects.get(pk=pk)
    title = 'Ваш отклик принят'
    email = [response.sender.email]
    html_context = render_to_string(
        'email/response_accepted_letter.html',
        {
            'link': f'{SITE_URL}/{response.announcement.pk}',
            'text': response.text,
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task
def send_weekly_mail():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    announcements = Announcement.objects.filter(date__gte=last_week)
    categories = set(announcements.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    # Фильтрует эмейлы, чтобы удалить все None, иначе выдает ошибку так как пытается послать почту на None
    email_list = []
    for email in subscribers_emails:
        if email:
            email_list.append(email)

    html_message = render_to_string(
        'email/weekly_mail.html',
        {"link": SITE_URL,
         'announcements': announcements
         }
    )

    msg = EmailMultiAlternatives(
        subject='Недельные статьи',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=email_list,
    )

    msg.attach_alternative(html_message, 'text/html')
    msg.send()
