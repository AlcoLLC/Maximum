from django.contrib import admin
from .models import (
    BrandGuidelineDocument,
    PromoMaterialsLibrary,
    PromoMaterial,
    BrandImageLibrary,
    BrandImage,
    BrandVideoLibrary,
    BrandVideo
)
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline


@admin.register(BrandGuidelineDocument)
class BrandGuidelineDocumentAdmin(TranslationAdmin):
    list_display = ('title', 'short_content')
    search_fields = ('title', 'description')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class PromoMaterialInline(TranslationTabularInline):
    model = PromoMaterial
    extra = 1
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(PromoMaterialsLibrary)
class PromoMaterialsLibraryAdmin(TranslationAdmin):
    list_display = ('short_content',)
    search_fields = ('short_content', 'description')
    inlines = [PromoMaterialInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class BrandImageInline(admin.TabularInline):
    model = BrandImage
    extra = 1


@admin.register(BrandImageLibrary)
class BrandImageLibraryAdmin(TranslationAdmin):
    list_display = ('short_content',)
    search_fields = ('short_content',)
    inlines = [BrandImageInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
class BrandVideoInline(admin.TabularInline):
    model = BrandVideo
    extra = 1


@admin.register(BrandVideoLibrary)
class BrandVideoLibraryAdmin(TranslationAdmin):
    list_display = ('short_content',)
    search_fields = ('short_content',)
    inlines = [BrandVideoInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }