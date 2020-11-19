from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_path(context, page_num):
    params = context["request"].GET
    path = f"?page={page_num}&intro=false"
    excluded_params = ["page", "intro"]

    if params:
        for param, value in params.items():
            if not param in excluded_params:
                path += f"&{param}={value}"

    return path


@register.filter
def text_primary(value):
    value_list = value.split(" ")
    last = value_list.pop(-1)
    value = " ".join(value_list)
    value += f" <span class='text-primary'>{last}</span>"
    return mark_safe(value)
