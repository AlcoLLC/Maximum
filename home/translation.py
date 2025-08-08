from modeltranslation.translator import register, TranslationOptions
from .models import HomeSwiper, Review, PageHeader

@register(HomeSwiper)
class HomeSwiperTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('summary', 'review')

@register(PageHeader)
class PageHeaderTranslationOptions(TranslationOptions):
    fields = ('title', 'description')