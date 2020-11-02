from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def text_primary(value):
    value_list = value.split(" ")
    last = value_list.pop(-1)
    value = " ".join(value_list)
    value += f" <span class='text-primary'>{last}</span>"
    return mark_safe(value)
