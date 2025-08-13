from modeltranslation.translator import register, TranslationOptions
from .models import Partnership_Content


@register(Partnership_Content)
class PartnershipContentTranslationOptions(TranslationOptions):
    fields = ('subtitle', 'title', 'description')


