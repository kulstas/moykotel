import os
import django
import datetime

from moykotel.settings import *
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from models import Post, Category

last_date = datetime.datetime(2023, 10, 13, 18)


def send_notifications(subject, pk, title, emails):
    html_content = render_to_string(
        'moykotel/../templates/mail/post_created_email.html',
        {
            'title': title,
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

posts_list = []
category_list = []

posts = Post.objects.filter(post_date__gt=last_date).order_by('-post_date')
categories = Category.objects.all()
for category in categories:
    emails = User.objects.filter(
        subscriptions__category=category
    ).values_list('email', flat=True)
    print(category.category_name, emails)

    subject = f'Новые посты по подписке — в категории {category.category_name}'

    for post in posts:
            send_notifications(subject, post.get_absolute_url(), post.post_title, emails,)