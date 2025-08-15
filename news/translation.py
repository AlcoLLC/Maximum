from modeltranslation.translator import register, TranslationOptions
from .models import News, News_Content

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(News_Content)
class NewsContentTranslationOptions(TranslationOptions):
    fields = ('description',)

