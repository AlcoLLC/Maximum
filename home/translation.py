from modeltranslation.translator import register, TranslationOptions
from .models import HomeSwiper, Review, General

@register(HomeSwiper)
class HomeSwiperTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('summary', 'review')

@register(General)
class GeneralTranslationOptions(TranslationOptions):
    fields = ('grow_description', 'range_description', 'production_description', 
              'presence_description', 'news_description', 'products_description', 'partners_description')
