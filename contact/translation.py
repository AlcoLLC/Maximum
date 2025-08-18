from modeltranslation.translator import translator, TranslationOptions
from .models import ContactInfo

class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('title', 'description',) 

translator.register(ContactInfo, ContactInfoTranslationOptions)
