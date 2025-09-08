from modeltranslation.translator import register, TranslationOptions, translator
from .models import (Product_group, Segments,
    Oil_Types, Product, ProductProperty, Product_Group_Category
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

class ProductGroupCategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(Product_Group_Category, ProductGroupCategoryTranslationOptions)