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
from .models import ContactStepTwo, ContactInfo
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
    
    # Clean the response
    recaptcha_response = recaptcha_response.strip()
    
    if len(recaptcha_response) < 20:  # reCAPTCHA responses are usually much longer
        logger.warning(f"reCAPTCHA response seems too short: {len(recaptcha_response)} characters")
        return False
    
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    
    # Add IP address if available (optional but recommended)
    if client_ip:
        data['remoteip'] = client_ip
    
    logger.debug(f"Sending reCAPTCHA verification request with IP: {client_ip}")
    
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', 
            data=data, 
            timeout=15  # Increased timeout
        )
        
        logger.debug(f"reCAPTCHA verification HTTP status: {response.status_code}")
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"reCAPTCHA verification result: {result}")
        
        # Check for specific error codes
        if not result.get('success', False):
            error_codes = result.get('error-codes', [])
            logger.warning(f"reCAPTCHA verification failed with error codes: {error_codes}")
            
            # Log specific error meanings for debugging
            error_meanings = {
                'missing-input-secret': 'The secret parameter is missing',
                'invalid-input-secret': 'The secret parameter is invalid or malformed',
                'missing-input-response': 'The response parameter is missing',
                'invalid-input-response': 'The response parameter is invalid or malformed',
                'bad-request': 'The request is invalid or malformed',
                'timeout-or-duplicate': 'The response is no longer valid (timeout or duplicate)',
            }
            
            for code in error_codes:
                meaning = error_meanings.get(code, f'Unknown error: {code}')
                logger.warning(f"reCAPTCHA error {code}: {meaning}")
            
            return False
        
        # Additional validation - check score if using v3
        score = result.get('score', 1.0)  # v2 doesn't have score, default to 1.0
        if score < 0.5:  # Adjust threshold as needed
            logger.warning(f"reCAPTCHA score too low: {score}")
            # You might want to return True here depending on your security requirements
            # For now, we'll accept it but log the low score
        
        logger.info(f"reCAPTCHA verification successful. Score: {score}")
        return True
        
    except requests.Timeout:
        logger.error("reCAPTCHA verification timeout")
        return False
    except requests.HTTPError as e:
        logger.error(f"reCAPTCHA verification HTTP error: {e.response.status_code} - {e.response.text}")
        return False
    except requests.RequestException as e:
        logger.error(f"reCAPTCHA verification network error: {str(e)}")
        return False
    except ValueError as e:
        logger.error(f"reCAPTCHA verification JSON decode error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"reCAPTCHA verification unexpected error: {str(e)}", exc_info=True)
        return False
    
def contact_step_two_view(request):
    """Contact form view with enhanced debugging for reCAPTCHA issues"""
    
    # Prepare form choices and labels for template
    role_choices = ContactStepTwo.ROLE_CHOICES
    question_type_choices = ContactStepTwo.QUESTION_TYPE_CHOICES
    
    form_labels = {
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
    }

    if request.method == 'POST':
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # ENHANCED DEBUGGING - Log everything about the request
        logger.info("=== CONTACT FORM SUBMISSION DEBUG ===")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Is AJAX: {is_ajax}")
        
        # Try to get reCAPTCHA response with multiple attempts
        recaptcha_response = None
        for key in ['g-recaptcha-response', 'g_recaptcha_response', 'recaptcha_response', 'recaptcha']:
            value = request.POST.get(key, '').strip()
            if value and not recaptcha_response:
                recaptcha_response = value
                logger.info(f"Found reCAPTCHA response with key '{key}'")
                break
        
        # Check for missing reCAPTCHA
        if not recaptcha_response:
            error_message = _("reCAPTCHA verification is required. Please complete the reCAPTCHA.")
            logger.warning("PROBLEM: Form submission with missing reCAPTCHA response.")
            
            if is_ajax:
                return JsonResponse({
                    'success': False, 
                    'message': error_message,
                    'recaptcha_missing': True
                }, status=400)
            else:
                messages.error(request, error_message)
                return redirect('contact:contact_step_two')
        
        client_ip = get_client_ip(request)
        logger.info(f"Client IP: {client_ip}")
        
        # Verify reCAPTCHA with enhanced logging
        logger.info("Starting reCAPTCHA verification...")
        recaptcha_valid = verify_recaptcha(recaptcha_response, client_ip)
        logger.info(f"reCAPTCHA verification result: {recaptcha_valid}")
        
        if not recaptcha_valid:
            error_message = _("reCAPTCHA verification failed. Please try again.")
            logger.warning(f"PROBLEM: reCAPTCHA verification failed for IP: {client_ip}")
            
            if is_ajax:
                return JsonResponse({
                    'success': False, 
                    'message': error_message,
                    'recaptcha_failed': True
                }, status=400)
            else:
                messages.error(request, error_message)
                return redirect('contact:contact_step_two')

        # If we get here, reCAPTCHA passed
        logger.info("reCAPTCHA verification PASSED - continuing with form processing...")

        # Check IP submission limit (5 submissions allowed)
        if client_ip:
            existing_submissions = ContactStepTwo.objects.filter(ip_address=client_ip).count()
            logger.info(f"Existing submissions from IP {client_ip}: {existing_submissions}")
            
            if existing_submissions >= 5:
                error_message = _("Maximum number of submissions reached from this IP address. Please contact us directly.")
                logger.warning(f"IP address {client_ip} exceeded submission limit (5).")
                
                if is_ajax:
                    return JsonResponse({
                        'success': False, 
                        'message': error_message
                    }, status=429)
                else:
                    messages.error(request, error_message)
                    return redirect('contact:contact_step_two')

        # Prepare form data
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
        
        logger.info(f"Form data processed: {form_data}")

        # Validate the form data using Django form
        from .forms import ContactStepTwoForm
        form = ContactStepTwoForm(form_data)
        
        if not form.is_valid():
            logger.warning(f"Form validation failed: {form.errors}")
            
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': _('Please correct the errors below.'),
                    'errors': form.errors
                }, status=400)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return redirect('contact:contact_step_two')

        # Use the cleaned data from the form
        cleaned_data = form.cleaned_data
        logger.info(f"Form validation passed. Creating contact entry...")

        # Create the ContactStepTwo instance
        try:
            contact = ContactStepTwo.objects.create(
                first_name=cleaned_data['first_name'],
                last_name=cleaned_data['last_name'],
                email=cleaned_data['email'],
                phone=cleaned_data.get('phone') or None,
                company=cleaned_data.get('company') or None,
                region=cleaned_data.get('region') or None,
                country=cleaned_data.get('country') or None,
                role=cleaned_data.get('role') or None,
                annual_volume=cleaned_data.get('annual_volume') or None,
                question_type=cleaned_data.get('question_type') or None,
                message=cleaned_data.get('message') or None,
                privacy_consent=cleaned_data['privacy_consent'],
                ip_address=client_ip
            )
            
            logger.info(f"Contact form entry created successfully with ID: {contact.id}")
            
            # Send emails
            try:
                send_contact_emails(contact)
                logger.info(f"Emails sent successfully for contact ID: {contact.id}")
            except Exception as e:
                logger.error(f"Failed to send emails for contact ID {contact.id}: {str(e)}", exc_info=True)
                # Don't fail the form submission if email sending fails
            
            # Return success response
            success_message = _("Thank you for contacting us! We have received your inquiry and will get back to you shortly.")
            
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': success_message
                })
            else:
                messages.success(request, success_message)
                return redirect('contact:contact_step_two')
                
        except Exception as e:
            logger.error(f"Failed to create contact form entry: {str(e)}", exc_info=True)
            error_message = _("An error occurred while processing your request. Please try again.")
            
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': error_message
                }, status=500)
            else:
                messages.error(request, error_message)
                return redirect('contact:contact_step_two')
        
        finally:
            logger.info("=== END CONTACT FORM DEBUG ===")

    # GET request - display form
    contact_info = None
    try:
        contact_info = ContactInfo.objects.last()
    except:
        logger.warning("ContactInfo model not found or no entries exist")
    
    context = {
        'role_choices': role_choices,
        'question_type_choices': question_type_choices,
        'contact_info': contact_info,
        'form_labels': form_labels,
        'recaptcha_site_key': RECAPTCHA_SITE_KEY,
    }
    
    return render(request, 'contact_step_two.html', context)

def send_contact_emails(contact):
    """Send both admin notification and user confirmation emails"""
    
    logger.info(f"Starting email send process for contact: {contact.email}")
    
    # Get display values for choices
    role_display = contact.get_role_display() if contact.role else _('Not specified')
    question_type_display = contact.get_question_type_display() if contact.question_type else _('Not specified')
    
    # 1. Admin notification email
    try:
        admin_subject = f"New Contact Form Submission - {contact.first_name} {contact.last_name}"
        admin_context = {
            'contact': contact,
            'role_display': role_display,
            'question_type_display': question_type_display,
        }
        
        admin_html_message = render_to_string('emails/contact_step_two_admin.html', admin_context)
        
        # Get admin email from settings
        admin_emails = getattr(settings, 'CONTACT_EMAIL', ['info@maximumlube.com'])
        if isinstance(admin_emails, str):
            admin_emails = [admin_emails]
        
        send_mail(
            subject=admin_subject,
            message='',  # Plain text fallback
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=admin_emails,
            html_message=admin_html_message,
            fail_silently=False,
        )
        logger.info(f"Admin notification email sent successfully for {contact.email}")
        
    except Exception as e:
        logger.error(f"Failed to send admin notification email: {str(e)}", exc_info=True)
        raise
    
    # 2. User confirmation email
    try:
        user_subject = _("Thank you for contacting Maximum")
        user_context = {
            'contact': contact,
            'role_display': role_display,
            'question_type_display': question_type_display,
        }
        
        user_html_message = render_to_string('emails/contact_step_two_user.html', user_context)
        
        # Simple plain text message as fallback
        user_plain_message = f"""
Dear {contact.first_name},

Thank you for contacting Maximum. We have received your inquiry and our team will get back to you shortly.

Best regards,
Maximum Support Team
"""
        
        send_mail(
            subject=user_subject,
            message=user_plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contact.email],
            html_message=user_html_message,
            fail_silently=False,
        )
        logger.info(f"User confirmation email sent successfully to {contact.email}")
        
    except Exception as e:
        logger.error(f"Failed to send user confirmation email: {str(e)}", exc_info=True)
        # Don't raise here - admin email is more important
        
    logger.info(f"Contact emails process completed for {contact.email}")

@require_http_methods(["POST"])
def validate_email_ajax(request):
    """AJAX endpoint for email validation"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'valid': False, 'message': _('Invalid request.')}, status=400)
    
    if not email:
        return JsonResponse({'valid': False, 'message': _('Email is required.')})
        
    from django.core.validators import validate_email, ValidationError
    try:
        validate_email(email)
        if ContactStepTwo.objects.filter(email=email).exists():
            return JsonResponse({
                'valid': True, 
                'warning': True, 
                'message': _('This email has been used before.')
            })
        return JsonResponse({'valid': True, 'message': _('Email is valid.')})
    except ValidationError:
        return JsonResponse({
            'valid': False, 
            'message': _('Please enter a valid email address.')
        })

def contact_info_view(request):
    """Simple view to display contact information"""
    contact_info = ContactInfo.objects.all()
    context = {'contact_info': contact_info}
    return render(request, 'contact.html', context)