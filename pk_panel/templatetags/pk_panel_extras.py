from django import template

register = template.Library()


@register.filter
def lowerfirst(value):
    """
    Lowercases the first letter of a string.
    """
    if not value:
        return value
    return value[0].lower() + value[1:]
