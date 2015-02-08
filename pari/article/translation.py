from modeltranslation.translator import translator, TranslationOptions

from .models import Article


class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "strap", "featured_image_caption",
              "content", "description")

translator.register(Article, ArticleTranslationOptions)
