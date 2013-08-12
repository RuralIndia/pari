from django.template.loader import render_to_string

from mezzanine import template

from pari.search.models import searcher

register = template.Library()


@register.simple_tag(takes_context=True)
def display_search_result(context):
    atom_name = searcher.get_atom_name(context['result'])
    return render_to_string(["article/includes/%s_atom.html" % atom_name,
                             "article/includes/default_atom.html"],
                            {'result': context['result'], 'request': context['request']})


@register.inclusion_tag("search/includes/search_result_list.html", takes_context=True)
def render_results(context):
    return {'results': context['results'],
            'query': context['query'],
            'result_types': context['result_types'],
            'filter': context['filter'],
            'request': context['request']}
