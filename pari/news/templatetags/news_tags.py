from mezzanine import template

register = template.Library()


@register.inclusion_tag("news/includes/latest_articles.html", takes_context=True)
def list_latest_articles(context):
    return {
        'archive_articles': context['new_archive_articles'],
        'current_articles': context['new_current_articles']
    }
