# contact/forms.py
from django import forms
from .models import ContactStepTwo

class ContactStepTwoForm(forms.ModelForm):
    class Meta:
        model = ContactStepTwo
        # Formada göstərmək istədiyiniz bütün sahələri qeyd edin
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company', 
            'region', 'country', 'role', 'annual_volume', 
            'question_type', 'message', 'privacy_consent'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Form sahələrinə class və ya digər atributlar əlavə etmək üçün
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' # Nümunə