from django.contrib import admin
from django.utils.html import format_html
from .models import  HomeSwiper, PartnerLogo, CarLogo, Review, PageHeader
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



@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    list_display = ('full_name', 'rating_stars', 'is_approved', 'created_at', 'email_address')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('first_name', 'surname', 'email_address', 'summary')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at', 'approved_at', 'ip_address', 'rating_stars')
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Review Information', {
            'fields': ('rating', 'rating_stars', 'summary', 'review', 'is_approved')
        }),
        ('Reviewer Information', {
            'fields': ('first_name', 'surname', 'email_address')
        }),
        ('System Information', {
            'fields': ('ip_address', 'created_at', 'updated_at', 'approved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_stars(self, obj):
     
        if not obj.rating:  
            return ""
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html(f'<span style="color: #ffc107; font-size: 16px;">{stars}</span> ({obj.rating})')

    rating_stars.short_description = "Rating"
    rating_stars.admin_order_field = 'rating'
    
    def get_queryset(self, request):
        """Optimization for performance"""
        return super().get_queryset(request)
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        """Approve selected reviews"""
        updated = queryset.update(is_approved=True, approved_at=timezone.now())
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        """Disapprove selected reviews"""
        updated = queryset.update(is_approved=False, approved_at=None)
        self.message_user(request, f'{updated} reviews disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"




@admin.register(PageHeader)
class PageHeaderAdmin(TranslationAdmin):  
    list_display = ('slug', 'title')
    search_fields = ('slug', 'title')

    fields = ('slug', 'title', 'description', 'image', 'link')