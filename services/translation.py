from modeltranslation.translator import register, TranslationOptions
from .models import Services,  Service_Content


@register(Services)
class ServicesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Service_Content)
class ServiceContentTranslationOptions(TranslationOptions):
    fields = ('subtitle', 'title', 'description')


