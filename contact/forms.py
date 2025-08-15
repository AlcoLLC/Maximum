from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from .models import ContactStepTwo
import re


class ContactStepTwoForm(forms.ModelForm):
    class Meta:
        model = ContactStepTwo
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company',
            'region', 'country', 'role', 'annual_volume', 
            'question_type', 'message', 'privacy_consent'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your mobile phone',
                'type': 'tel'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your region'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your country'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'annual_volume': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter annual volume'
            }),
            'question_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please describe your question or request...',
                'rows': 4
            }),
            'privacy_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'required': True
            })
        }
        
        error_messages = {
            'first_name': {
                'required': _('First name is required.'),
                'max_length': _('First name must be less than 100 characters.'),
            },
            'last_name': {
                'required': _('Last name is required.'),
                'max_length': _('Last name must be less than 100 characters.'),
            },
            'email': {
                'required': _('Email address is required.'),
                'invalid': _('Please enter a valid email address.'),
            },
            'privacy_consent': {
                'required': _('You must agree to the privacy policy.'),
            }
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError(_('First name is required.'))
        if len(first_name) < 2:
            raise forms.ValidationError(_('First name must be at least 2 characters long.'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError(_('Last name is required.'))
        if len(last_name) < 2:
            raise forms.ValidationError(_('Last name must be at least 2 characters long.'))
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError(_('Email address is required.'))
        
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except forms.ValidationError:
            raise forms.ValidationError(_('Please enter a valid email address.'))
        
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone:
            phone_digits = re.sub(r'\D', '', phone)
            if len(phone_digits) < 7:
                raise forms.ValidationError(_('Phone number must be at least 7 digits.'))
            if len(phone_digits) > 15:
                raise forms.ValidationError(_('Phone number must be less than 16 digits.'))
        return phone

    def clean_privacy_consent(self):
        privacy_consent = self.cleaned_data.get('privacy_consent')
        if not privacy_consent:
            raise forms.ValidationError(_('You must agree to the privacy policy to submit this form.'))
        return privacy_consent

    def clean(self):
        cleaned_data = super().clean()
        
        return cleaned_data