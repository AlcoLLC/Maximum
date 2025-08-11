from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Product_group, Segments, Oil_Types, Viscosity, Liter, Product, ProductProperty
from django.utils.html import format_html

@admin.register(Product_group)
class ProductGroupAdmin(TranslationAdmin):
    list_display = ('title', 'slug', 'image', 'in_home_sec1','in_home_sec2')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_editable = ['in_home_sec1','in_home_sec2']

    
    def save_model(self, request, obj, form, change):
        if obj.in_home_sec1:
            current_home_count = Product_group.objects.filter(in_home_sec1=True).count()
            if not change:
                if current_home_count >= 2:
                    from django.contrib import messages
                    messages.error(request, "A maximum of 2 product groups can be displayed on the home page section 1")
                    obj.in_home_sec1 = False
            elif change:
                if current_home_count >= 2 and not Product_group.objects.get(pk=obj.pk).in_home_sec1:
                    from django.contrib import messages
                    messages.error(request, "A maximum of 2 product groups can be displayed on the home page section 1")
                    obj.in_home_sec1 = False
        
        super().save_model(request, obj, form, change)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Segments)
class SegmentsAdmin(TranslationAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Oil_Types)
class OilTypesAdmin(TranslationAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Viscosity)
class ViscosityAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
  

@admin.register(Liter)
class LiterAdmin(admin.ModelAdmin):
    list_display = ('volume',)
    ordering = ('volume',)
    

class ProductPropertyInline(TranslationTabularInline):
    model = ProductProperty
    extra = 1
    fields = ['property_name', 'unit', 'test_method', 'typical_value', 'order']
    ordering = ['order']


@admin.register(ProductProperty)
class ProductPropertyAdmin(TranslationAdmin):
    list_display = ['product', 'property_name', 'unit', 'test_method', 'typical_value', 'order']
    list_filter = ['product', 'unit']
    search_fields = ['property_name', 'test_method', 'product__title']
    list_editable = ['order']
    ordering = ['product', 'order']
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['title', 'product_id', 'product_group', 'oil_type', 'has_pds', 'has_sds', 'in_home']
    list_filter = ['product_group', 'segments', 'oil_type', 'viscosity']
    search_fields = ['title', 'product_id', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['in_home']
    inlines = [ProductPropertyInline]

    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'product_id', 'description', 'image', 'features_benefits', 'application', 'in_home', 'order')
        }),
        ('Specifications', {
            'fields': ('api', 'ilsac', 'acea', 'jaso', 'oem_sertification', 'recommendations')
        }),
        ('Categories', {
            'fields': ('product_group', 'segments', 'oil_type', 'viscosity', 'liters')
        }),
        ('Documents', {
            'fields': ('pds_url', 'sds_url'),
            'classes': ('collapse',),
        }),
    )
    
    def has_pds(self, obj):
        if obj.pds_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">View PDS</a>',
                obj.pds_url
            )
        return '❌'
    has_pds.short_description = 'PDS'
    
    def has_sds(self, obj):
        if obj.sds_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">View SDS</a>',
                obj.sds_url
            )
        return '❌'
    has_sds.short_description = 'SDS'
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }