from mezzanine import template

register = template.Library()


@register.inclusion_tag("news/includes/articles_gist.html")
def articles_gist(articles):
    return {
        'articles': articles,
    }
