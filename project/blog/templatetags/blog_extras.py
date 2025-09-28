from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """
    Divise une chaîne en utilisant un délimiteur spécifié.
    Usage: {{ value|split:',' }}
    """
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]

@register.filter
def strip(value):
    """
    Supprime les espaces en début et fin de chaîne.
    Usage: {{ value|strip }}
    """
    if not value:
        return ''
    return str(value).strip()
