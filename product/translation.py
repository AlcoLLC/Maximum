from modeltranslation.translator import register, TranslationOptions
from .models import (Product_group, Segments,
    Oil_Types, Product, ProductProperty
)

@register(Product_group)
class ProductGroupTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Segments)
class SegmentsTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Oil_Types)
class OilTypesTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'features_benefits', 'application',
        'recommendations'
    )

@register(ProductProperty)
class ProductPropertyTranslationOptions(TranslationOptions):
    fields = ('property_name', 'unit', 'test_method', 'typical_value')
