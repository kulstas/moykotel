from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from celery import shared_task
import datetime

from moykotel.models import Post, Subscriber, User
from moykotel.settings import *


def send_notifications(subject, preview, pk, title, emails):
    html_content = render_to_string(
        'mail/post_created_email.html',
        {
            'title': title,
            'text': preview,
            'link': f'{SITE_URL}{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def new_post_subscription(instance):
    categories = instance.post_category.all()
    subscribers: list[str] = []

    for category in categories:
        subject = f'Новый пост по подписке — в категории {category.category_name}'
        subscribers += category.subscribers.all()

        emails = User.objects.filter(
            subscription_user__category=category
        ).values_list('email', flat=True)

        send_notifications(subject, instance.preview(), instance.get_absolute_url(), instance.post_title, emails,)

@shared_task
def weekly_newsletter():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.filter(post_date__gte=last_week).values_list('post_category', flat=True))
    users = set(Subscriber.objects.all().values_list('user', flat=True))

    for subscriber in users:
        categories_subscriber = set(
             Subscriber.objects.filter(user=subscriber).values_list('category_id', flat=True))
        categories_newsletter = categories & categories_subscriber
        posts_list = posts.filter(
            post_category__in=categories_newsletter
        )

        html_content = render_to_string(
            'mail/categories_weekly_email.html',
                {
                    'link': SITE_URL,
                    'posts': posts_list,
                }
            )

        msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=DEFAULT_FROM_EMAIL,
                to=list(User.objects.filter(pk=subscriber).values_list('email', flat=True)),
            )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()