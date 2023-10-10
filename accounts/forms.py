from django.contrib.auth.models import Group
from django import forms

from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First name', required=False)
    last_name = forms.CharField(max_length=30, label='Last name', required=False)

    def save(self, request):
        user = super().save(request)
        clients = Group.objects.get(name='clients')
        user.groups.add(clients)
        return user