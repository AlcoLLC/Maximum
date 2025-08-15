from modeltranslation.translator import register, TranslationOptions
from .models import BrandGuidelineDocument, PromoMaterialsLibrary, PromoMaterial, BrandImageLibrary, BrandVideoLibrary

@register(BrandGuidelineDocument)
class BrandGuidelineDocumentTranslationOptions(TranslationOptions):
    fields = ('title','short_content', 'description')


@register(PromoMaterialsLibrary)
class PromoMaterialsLibraryTranslationOptions(TranslationOptions):
   fields = ('short_content', 'description')

@register(PromoMaterial)
class PromoMaterialTranslationOptions(TranslationOptions):
   fields = ('title',)

@register(BrandImageLibrary)
class BrandImageLibraryTranslationOptions(TranslationOptions):
   fields = ('short_content', 'description')

@register(BrandVideoLibrary)
class BrandVideoLibraryTranslationOptions(TranslationOptions):
   fields = ('short_content', 'description')

