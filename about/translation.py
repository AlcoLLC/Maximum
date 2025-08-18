from modeltranslation.translator import translator, TranslationOptions
from .models import About, AboutContent, AboutSection, GlobalPresence, Sustainability, PartnershipContent

class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

translator.register(About, AboutTranslationOptions)


class AboutContentTranslationOptions(TranslationOptions):
    fields = ('section_title', 'section_content',)

translator.register(AboutContent, AboutContentTranslationOptions)


class AboutSectionTranslationOptions(TranslationOptions):
    fields = ('section_title', 'section_description', 'category',)

translator.register(AboutSection, AboutSectionTranslationOptions)


class GlobalPresenceTranslationOptions(TranslationOptions):
    fields = ('title', 'description_one', 'description_two', 'description_three',)

translator.register(GlobalPresence, GlobalPresenceTranslationOptions)


class SustainabilityTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

translator.register(Sustainability, SustainabilityTranslationOptions)


class PartnershipContentTranslationOptions(TranslationOptions):
    fields = ('title', 'title_content', 'description',)

translator.register(PartnershipContent, PartnershipContentTranslationOptions)
