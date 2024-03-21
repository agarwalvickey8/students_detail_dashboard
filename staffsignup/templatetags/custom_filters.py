# custom_filters.py
from django import template

register = template.Library()

@register.filter
def lookup(obj, attr):
    return getattr(obj, attr, None)
