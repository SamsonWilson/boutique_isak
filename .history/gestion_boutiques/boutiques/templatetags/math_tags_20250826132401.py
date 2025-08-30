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
def has_role(user, roles):
    """
    Vérifie si l'utilisateur a un rôle dans une liste
    Ex: {% if user|has_role:"admin,responsable" %} … {% endif %}
    """
    if not hasattr(user, "role"):
        return False
    return user.role in roles.split(",")    