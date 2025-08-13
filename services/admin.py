from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    Services,
    Service_Content,
)

@admin.register(Services)
class ServicesAdmin(TranslationAdmin):
    list_display = ('title',)
    search_fields = ('title',)

    fields = (
        'title', 'description', 'image'
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


@admin.register(Service_Content)
class ServiceContentAdmin(TranslationAdmin):
    list_display = ('title',)
    search_fields = ('title', )
    
    fields = (
        'subtitle',
        'title', 
        'description', 
        'image'
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




