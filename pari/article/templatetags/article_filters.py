from django.template import Library


register = Library()


@register.filter
def get_range( value ):
  return range( value )

@register.filter
def get_absolute_url(obj):
    return obj.get_absolute_url()