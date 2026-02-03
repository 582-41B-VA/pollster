from django import template

register = template.Library()


@register.filter
def get(value, arg) -> str | None:
    """Custom filter to access a dict value with a dynamic key."""
    if type(value) is not dict:
        return None
    return value.get(str(arg))
