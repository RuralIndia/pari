import random

from django.template import Library


register = Library()


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_absolute_url(obj):
    return obj.get_absolute_url()


@register.filter
def group_by(l, n):
    if l is None:
        return None
    return [l[i:i + n] for i in range(0, len(l), n)]


@register.filter
def get_type(object):
    return object.__class__.__name__.lower()


@register.filter
def get_random(obj, upper):
    return "%s%d" % (obj, random.randint(1, upper))


@register.filter
def get_request_url(obj, request):
    return request.build_absolute_uri(get_absolute_url(obj))


@register.filter
def lower(type):
    return type.lower()
