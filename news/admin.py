# admin.py
from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import News, News_Content


class NewsContentInline(TranslationTabularInline):
    model = News_Content
    extra = 1

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'published_date', 'is_active', 'is_top', 'in_home', 'image_preview']
    list_filter = ['is_active', 'published_date']
    search_fields = ['title', 'content']
    list_editable = ['is_active', 'is_top', 'in_home']
    readonly_fields = ['image_preview']
    inlines = [NewsContentInline]
    
    fieldsets = (
        ('News Information', {
            'fields': ('title', 'slug', 'content', 'is_active', 'is_top', 'in_home')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Meta Information', {
            'fields': ('published_date',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img loading="lazy"  src="{}" style="width: 100px; height: 60px; object-fit: cover;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
            'admin/js/news_slug.js',
        )
        css = {
            'all': ('admin/css/news_admin.css',),
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }