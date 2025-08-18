from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ContactStepTwo, ContactInfo


@admin.register(ContactStepTwo)
class ContactStepTwoAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name', 
        'email', 
        'company', 
        'role',
        'question_type',
        'created_at', 
        'ip_address'
    )
    
    list_filter = (
        'role',
        'question_type',
        'privacy_consent',
        'created_at',
    )
    
    search_fields = (
        'first_name',
        'last_name', 
        'email',
        'company',
        'country',
        'region'
    )
    
    readonly_fields = (
        'ip_address',
        'created_at', 
        'updated_at'
    )
    
    fieldsets = (
        (_('Personal Information'), {
            'fields': (
                'first_name',
                'last_name', 
                'email',
                'phone'
            )
        }),
        (_('Business Information'), {
            'fields': (
                'company',
                'region',
                'country',
                'role',
                'annual_volume'
            )
        }),
        (_('Inquiry Details'), {
            'fields': (
                'question_type',
                'message'
            )
        }),
        (_('Consent & Tracking'), {
            'fields': (
                'privacy_consent',
                'ip_address'
            )
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
    
    date_hierarchy = 'created_at'
    
    def has_delete_permission(self, request, obj=None):
        # Allow delete only for superusers
        return request.user.is_superuser
        
    def has_change_permission(self, request, obj=None):
        # Allow edit for staff users
        return request.user.is_staff
        
    class Media:
        css = {
            'all': ('admin/css/contact_admin.css',)
        }

from modeltranslation.admin import TranslationAdmin

class ContactInfoAdmin(TranslationAdmin):
    list_display = ('title', 'phone', 'email')
    search_fields = ('title', 'description', 'phone', 'email')

    def has_add_permission(self, request):
        if self.model.objects.count() >= 3:
            return False
        return super().has_add_permission(request)

admin.site.register(ContactInfo, ContactInfoAdmin)
