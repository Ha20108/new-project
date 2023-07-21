from django import template

register = template.Library()

@register.filter(name='replace_dash')
def replace_dash(value):
    return value.replace("-", "_")


@register.simple_tag
def attributeLookup(the_object, attribute_name):
   # Try to fetch from the object, and if it's not found return None.
   return getattr(the_object, attribute_name, None)
@register.filter(name='attributeLookup')
def attributeLookup(obj, arg):
    """
    Usage: {{ obj|attributeLookup:"arg" }}
    """
    try:
        return getattr(obj, arg)
    except AttributeError:
        return ''


