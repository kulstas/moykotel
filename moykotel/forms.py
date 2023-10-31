from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea

from .models import Post, Comment


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['comment_text'].widget = Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Оставьте свой комментарий тут ...'
        })