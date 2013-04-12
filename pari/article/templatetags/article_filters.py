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
        return None;
    return [l[i:i+n] for i in range(0, len(l), n)]
