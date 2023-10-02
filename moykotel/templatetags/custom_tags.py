from datetime import datetime
from django import template

register = template.Library()

# тег копирайта
@register.simple_tag()
def copyright(format_string='%Y'):
   return f'© MoyKotel {datetime.utcnow().strftime(format_string)}'
