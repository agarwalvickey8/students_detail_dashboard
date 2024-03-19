# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr):
    """Get attribute dynamically."""
    return getattr(obj, attr, '')
