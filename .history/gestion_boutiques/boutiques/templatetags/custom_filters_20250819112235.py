# app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplie une valeur par un argument"""
    try:
        return float(value) * float(arg)
    except:
        return 0