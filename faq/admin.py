from django.contrib import admin
from .models import FAQ
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('question', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }