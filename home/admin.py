from django.contrib import admin
from django.utils.html import format_html
from .models import  HomeSwiper, PartnerLogo, CarLogo
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

@admin.register(HomeSwiper)
class HomeSwiperAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'image', 'order', 'is_active')
        }),
        ('İçerik', {
            'fields': ('link',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img loading="lazy"    src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo_preview', 'logo_name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name', 'logo_preview', 'logo_name']
    readonly_fields = ['logo_preview_large', 'created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img loading="lazy"  src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview.short_description = "Preview"
    
    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html(
                '<img loading="lazy"  src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview_large.short_description = "Logo Preview"
    
    def logo_name(self, obj):
        if obj.logo:
            return obj.logo.name.split('/')[-1] 
        return "No File"
    logo_name.short_description = "File Name"
    
    fieldsets = (
        ('Logo Information', {
            'fields': ('name', 'logo', 'logo_preview_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CarLogo)
class CarLogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo_preview', 'logo_name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name', 'logo_preview', 'logo_name']
    readonly_fields = ['logo_preview_large', 'created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img loading="lazy"  src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview.short_description = "Preview"
    
    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html(
                '<img loading="lazy"  src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview_large.short_description = "Logo Preview"
    
    def logo_name(self, obj):
        if obj.logo:
            return obj.logo.name.split('/')[-1] 
        return "No File"
    logo_name.short_description = "File Name"
    
    fieldsets = (
        ('Logo Information', {
            'fields': ('name','logo', 'logo_preview_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
