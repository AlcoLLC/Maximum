# contact/models.py

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ContactStepTwo(models.Model):
    ROLE_CHOICES = [
        ('business-buyer', _('Business Buyer / Company Representative')),
        ('distributor', _('Distributor / Dealer')),
        ('other', _('Other')),
    ]

    QUESTION_TYPE_CHOICES = [
        ('product-info', _('Product Information / Technical Support')),
        ('support', _('Technical Support')),
        ('pricing', _('Pricing & Orders')),
        ('partnership', _('Partnership Inquiry')),
        ('other', _('Other')),
    ]

    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Mobile Phone'))
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Company'))
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Region'))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Country'))
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True, verbose_name=_('Role'))
    annual_volume = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Annual Volume'))
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES, blank=True, null=True, verbose_name=_('Type of Question'))
    message = models.TextField(blank=True, null=True, verbose_name=_('Message'))
    privacy_consent = models.BooleanField(default=False, verbose_name=_('Privacy Policy Consent'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'), null=True, blank=True)
    
    # DƏYİŞİKLİK: auto_now_add=True istifadə etmək daha doğrudur.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = _('Contact Step Two')
        verbose_name_plural = _('Contact Step Two Entries')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['created_at']),
            models.Index(fields=['email']),
        ]