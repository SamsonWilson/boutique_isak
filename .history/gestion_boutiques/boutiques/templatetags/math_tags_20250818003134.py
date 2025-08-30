from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplie deux valeurs (quantité * prix)"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""
    

from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplie deux valeurs (quantité * prix)"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""    