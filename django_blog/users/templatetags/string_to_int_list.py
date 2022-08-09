from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def string_to_int_list(value):

    value = value.replace('[', '').replace(']', '').replace('"', '')

    int_list = value.split(', ')

    int_list = list(map(int, int_list))

    return int_list