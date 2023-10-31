from django.contrib.auth.models import Group
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_managers, mail_admins

from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    # first_name = forms.CharField(max_length=30, label='First name', required=False)
    # last_name = forms.CharField(max_length=30, label='Last name', required=False)

    def save(self, request):
        user = super().save(request)
        clients = Group.objects.get(name='clients')
        user.groups.add(clients)

        subject = 'Добро пожаловать на наш портал!'
        text = f'{user.username}, вы успешно зарегестрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегестрировались на '
            f'<a href="http://127.0.0.1:8000/news/">сайте</a>'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user