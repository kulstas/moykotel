from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from moykotel.settings import *
from moykotel.models import Category, Post

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


def new_posts_subscrition(instance):
    categories = instance.post_category.all()
    subscribers: list[str] = []
    print(categories)

    for category in categories:
        print(category)
        subject = f'Новый пост по подписке — в категории {category.category_name}'
        subscribers += category.subscribers.all()

        emails = User.objects.filter(
            subscriptions__category=category
        ).values_list('email', flat=True)

        send_notifications(subject, instance.preview(), instance.get_absolute_url(), instance.post_title, emails,)