from django import template
from datetime import datetime
from django.utils.timezone import utc
import re

register = template.Library()

# фильтр, возвращающий значение переменной
@register.filter()
def show(value):
    return f'{value}'

# фильтр изменения формата даты
@register.filter()
def date_format(value):
   return datetime.strftime(value, '%d-%b-%Y')


# фильтр цензурирования
@register.filter()
def censor(text):
    if isinstance(text, str):
        # список нежелательных слов
        cens_list = ['редиска', 'чудак']

        filter_text = re.split(r"\W", text)
        for word in filter_text:
            if word in cens_list:
                cens_word = word[0] + '*' * (len(word) - 1)
                text = text.replace(word, cens_word)
        return text
    else:
        print(f'Переменная {text} не может быть обработана, так как не является строкой :(')
