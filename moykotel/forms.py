from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_title',
            'post_text',
            'post_category',
        ]

        def clean(self):
            cleaned_data = super().clean()
            post_text = cleaned_data.get('post_text')
            post_title = cleaned_data.get('post_title')

            if post_title == post_text:
                raise ValidationError({
                    "Описание не должно быть идентичным названию."
                })

            return cleaned_data

        def clean_name(self):
            name = self.cleaned_data["name"]
            if name[0].islower():
                raise ValidationError(
                    "Название должно начинаться с заглавной буквы."
                )
            return name