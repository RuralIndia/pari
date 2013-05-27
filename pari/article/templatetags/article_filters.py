import random
import calendar

from django.template import Library
from django.core.urlresolvers import reverse


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


@register.filter
def month_name(month_number):
    return calendar.month_name[int(month_number)]


@register.filter
def get_location_titles(article):
    return ','.join([location.title for location in article.locations.all()])


@register.filter
def get_latitudes(article):
    return ','.join(map(str, [location.location.latitude for location in article.locations.all()]))


@register.filter
def get_longitudes(article):
    return ','.join(map(str, [location.location.longitude for location in article.locations.all()]))


@register.filter
def archive_url(date):
    month = date.month
    year = date.year
    return reverse('archive-detail', kwargs={"year": year, "month": month})
