from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta

# Model və Formları import edirik
from .models import ContactStepTwo, ContactInfo
from .forms import ContactStepTwoForm

import logging
import json
import requests

RECAPTCHA_SITE_KEY = settings.RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY = settings.RECAPTCHA_SECRET_KEY
logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def verify_recaptcha(recaptcha_response, client_ip=None):
    """Verify reCAPTCHA response with better error handling and debugging"""
    if not recaptcha_response:
        logger.warning("Empty reCAPTCHA response received")
        return False
    
    if not RECAPTCHA_SECRET_KEY:
        logger.error("RECAPTCHA_SECRET_KEY not configured")
        return False
    
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    
    if client_ip:
        data['remoteip'] = client_ip
    
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', 
            data=data, 
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        logger.debug(f"reCAPTCHA verification result: {result}")
        
        if not result.get('success', False):
            error_codes = result.get('error-codes', [])
            logger.warning(f"reCAPTCHA verification failed with error codes: {error_codes}")
            return False
            
        return True
        
    except requests.RequestException as e:
        logger.error(f"reCAPTCHA verification network error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"reCAPTCHA verification unexpected error: {str(e)}", exc_info=True)
        return False

def contact_step_two_view(request):
    """Contact form view with full processing logic"""
    
    if request.method == 'POST':
        # AJAX sorğusu olub-olmadığını yoxlayırıq
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Ətraflı loglama
        logger.info("=== CONTACT FORM SUBMISSION START ===")
        client_ip = get_client_ip(request)
        logger.info(f"Client IP: {client_ip}")
        logger.info(f"Is AJAX: {is_ajax}")

        # reCAPTCHA yoxlaması
        recaptcha_response = request.POST.get('g-recaptcha-response', '')
        if not verify_recaptcha(recaptcha_response, client_ip):
            logger.warning(f"PROBLEM: reCAPTCHA verification failed for IP: {client_ip}")
            return JsonResponse({
                'success': False,
                'message': _("reCAPTCHA verification failed. Please try again."),
                'recaptcha_failed': True
            }, status=400)
        logger.info("reCAPTCHA verification PASSED.")

        # IP limiti yoxlaması
        if client_ip and ContactStepTwo.objects.filter(ip_address=client_ip).count() >= 5:
            logger.warning(f"IP address {client_ip} exceeded submission limit (5).")
            return JsonResponse({
                'success': False,
                'message': _("Maximum number of submissions reached from this IP address.")
            }, status=429)

        # Frontend-dən gələn datanı form üçün hazırlayırıq
        form_data = {
            'first_name': request.POST.get('firstName', '').strip(),
            'last_name': request.POST.get('lastName', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'company': request.POST.get('company', '').strip(),
            'region': request.POST.get('region', '').strip(),
            'country': request.POST.get('country', '').strip(),
            'role': request.POST.get('role', '').strip(),
            'annual_volume': request.POST.get('annualVolume', '').strip(),
            'question_type': request.POST.get('questionType', '').strip(),
            'message': request.POST.get('message', '').strip(),
            'privacy_consent': request.POST.get('privacyConsent') == 'on'
        }
        
        form = ContactStepTwoForm(form_data)
        
        if form.is_valid():
            try:
                # Formu yadda saxlayırıq və IP ünvanını əlavə edirik
                contact_instance = form.save(commit=False)
                contact_instance.ip_address = client_ip
                contact_instance.save()
                logger.info(f"Contact form saved successfully for {contact_instance.email}")

                # E-poçtları göndəririk
                send_contact_emails(contact_instance)
                
                # Uğurlu cavab qaytarırıq
                return JsonResponse({
                    'success': True,
                    'message': _('Thank you for your message! We will get in touch with you shortly.')
                })
            except Exception as e:
                logger.error(f"Error processing form or sending email: {str(e)}", exc_info=True)
                return JsonResponse({
                    'success': False,
                    'message': _('An unexpected error occurred. Please try again later.')
                }, status=500)
        else:
            # Formda xətalar varsa, onları JSON formatında qaytarırıq
            logger.warning(f"Form validation failed. Errors: {form.errors.as_json()}")
            return JsonResponse({
                'success': False,
                'message': _('Please correct the errors indicated below.'),
                'errors': form.errors
            }, status=400)

    # GET metodu üçün formanı və digər məlumatları hazırlayırıq
    contact_info = ContactInfo.objects.last()
    context = {
        'role_choices': ContactStepTwo.ROLE_CHOICES,
        'question_type_choices': ContactStepTwo.QUESTION_TYPE_CHOICES,
        'contact_info': contact_info,
        'form_labels': {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
            'phone': _('Mobile Phone'),
            'company': _('Company'),
            'region': _('Region'),
            'country': _('Country'),
            'role': _('Role'),
            'annual_volume': _('Annual Volume'),
            'question_type': _('Type of Question'),
            'message': _('Message'),
            'privacy_consent': _('Privacy Policy Consent'),
            'required': '*',
            'send_button': _('Send')
        },
        'recaptcha_site_key': RECAPTCHA_SITE_KEY,
    }
    
    return render(request, 'contact_step_two.html', context)


def send_contact_emails(contact):
    """Send both admin notification and user confirmation emails"""
    logger.info(f"Starting email send process for contact: {contact.email}")
    
    try:
        # Adminə bildiriş e-poçtu
        admin_subject = f"New Contact Form Submission - {contact.first_name} {contact.last_name}"
        admin_context = {
            'contact': contact,
            'role_display': contact.get_role_display(),
            'question_type_display': contact.get_question_type_display(),
        }
        admin_html_message = render_to_string('emails/contact_step_two_admin.html', admin_context)
        admin_emails = getattr(settings, 'CONTACT_EMAIL', ['info@example.com'])
        if isinstance(admin_emails, str):
            admin_emails = [admin_emails]
        
        send_mail(
            subject=admin_subject,
            message='', # HTML olduğu üçün boş saxlamaq olar
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=admin_emails,
            html_message=admin_html_message,
            fail_silently=False,
        )
        logger.info(f"Admin notification email sent successfully for {contact.email}")
        
        # İstifadəçiyə təsdiq e-poçtu
        user_subject = _("Thank you for contacting us")
        user_context = {'contact': contact}
        user_html_message = render_to_string('emails/contact_step_two_user.html', user_context)
        
        send_mail(
            subject=user_subject,
            message=f"Dear {contact.first_name}, thank you for your message.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contact.email],
            html_message=user_html_message,
            fail_silently=False,
        )
        logger.info(f"User confirmation email sent successfully to {contact.email}")

    except Exception as e:
        logger.error(f"Failed to send emails: {str(e)}", exc_info=True)
        # Hata olsa da prosesi dayandırmırıq, çünki data artıq bazadadır.
        # Amma loglama çox vacibdir.

@require_http_methods(["POST"])
def validate_email_ajax(request):
    """AJAX endpoint for email validation"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'valid': False, 'message': _('Invalid request.')}, status=400)
    
    from django.core.validators import validate_email, ValidationError
    try:
        validate_email(email)
        return JsonResponse({'valid': True})
    except ValidationError:
        return JsonResponse({
            'valid': False, 
            'message': _('Please enter a valid email address.')
        })

def contact_info_view(request):
    """Simple view to display contact information"""
    contact_info = ContactInfo.objects.last()
    context = {'contact_info': contact_info}
    return render(request, 'contact.html', context)