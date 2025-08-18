from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import About, AboutContent, AboutSection, GlobalPresence, Sustainability, PartnershipContent

class SingleInstanceAdmin(TranslationAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


class AboutContentAdmin(TranslationAdmin):
    list_display = ('section_title', 'about')
    search_fields = ('section_title', 'section_content')
    list_filter = ('about',)


@admin.register(About)
class AboutAdmin(SingleInstanceAdmin):
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(AboutSection)
class AboutSectionAdmin(SingleInstanceAdmin):
    list_display = ('section_title', 'category')

@admin.register(GlobalPresence)
class GlobalPresenceAdmin(SingleInstanceAdmin):
    list_display = ('title',)

@admin.register(Sustainability)
class SustainabilityAdmin(SingleInstanceAdmin):
    list_display = ('title',)

@admin.register(PartnershipContent)
class PartnershipContentAdmin(SingleInstanceAdmin):
    list_display = ('title',)


admin.site.register(AboutContent, AboutContentAdmin)
