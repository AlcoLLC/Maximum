from django.shortcuts import render

# Create your views here.

def contact_view(request):
    return render(request, 'contact.html')

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import ContactStepTwo
from .forms import ContactStepTwoForm
import logging
import json

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def contact_step_two_view(request):
    """Display contact step two form"""
    if request.method == 'GET':
        form = ContactStepTwoForm()
        context = {
            'form': form,
            'role_choices': ContactStepTwo.ROLE_CHOICES,
            'question_type_choices': ContactStepTwo.QUESTION_TYPE_CHOICES,
        }
        return render(request, 'contact_step_two.html', context)
    
    elif request.method == 'POST':
        return handle_contact_step_two_submission(request)


@csrf_protect
def handle_contact_step_two_submission(request):
    """Handle form submission via AJAX"""
    try:
        # Parse JSON data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        form = ContactStepTwoForm(data)
        client_ip = get_client_ip(request)
        
        if form.is_valid():
            # Save the contact entry
            contact = form.save(commit=False)
            contact.ip_address = client_ip
            contact.save()
            
            # Send email notifications
            try:
                send_contact_emails(contact)
                
                # Success response
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'message': str(_('Thank you for contacting us! We will get back to you soon.'))
                    })
                else:
                    messages.success(request, _('Thank you for contacting us! We will get back to you soon.'))
                    return redirect('contact:contact_step_two')
                    
            except Exception as e:
                logger.error(f"Error sending contact emails: {str(e)}", exc_info=True)
                
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'message': str(_('Your message was saved but we encountered an error sending emails. We will still get back to you.'))
                    })
                else:
                    messages.warning(request, _('Your message was saved but we encountered an error sending emails. We will still get back to you.'))
                    return redirect('contact:contact_step_two')
        
        else:
            # Form validation errors
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            
            if request.content_type == 'application/json':
                return JsonResponse({
                    'success': False,
                    'errors': errors,
                    'message': str(_('Please correct the errors below.'))
                }, status=400)
            else:
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{field}: {error}")
                
                context = {
                    'form': form,
                    'role_choices': ContactStepTwo.ROLE_CHOICES,
                    'question_type_choices': ContactStepTwo.QUESTION_TYPE_CHOICES,
                }
                return render(request, 'contact_step_two.html', context)
                
    except json.JSONDecodeError:
        if request.content_type == 'application/json':
            return JsonResponse({
                'success': False,
                'message': str(_('Invalid JSON data.'))
            }, status=400)
        else:
            messages.error(request, _('Invalid form data.'))
            return redirect('contact:contact_step_two')
    
    except Exception as e:
        logger.error(f"Unexpected error in contact form: {str(e)}", exc_info=True)
        
        if request.content_type == 'application/json':
            return JsonResponse({
                'success': False,
                'message': str(_('An unexpected error occurred. Please try again.'))
            }, status=500)
        else:
            messages.error(request, _('An unexpected error occurred. Please try again.'))
            return redirect('contact:contact_step_two')


def send_contact_emails(contact):
    """Send email notifications for contact form submission"""
    try:
        # Email to admin
        admin_subject = f"New Contact Form Submission - {contact.first_name} {contact.last_name}"
        
        admin_context = {
            'contact': contact,
            'role_display': contact.get_role_display() if contact.role else 'Not specified',
            'question_type_display': contact.get_question_type_display() if contact.question_type else 'Not specified',
        }
        
        admin_html_message = render_to_string('emails/contact_step_two_admin.html', admin_context)
        
        send_mail(
            subject=admin_subject,
            message='',  # Plain text message (empty since we're using HTML)
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[getattr(settings, 'CONTACT_EMAIL', settings.EMAIL_HOST_USER)],
            html_message=admin_html_message,
            fail_silently=False,
        )
        
        # Confirmation email to user
        user_subject = _("Thank you for contacting us - Tomoil")
        
        user_context = {
            'contact': contact,
        }
        
        user_html_message = render_to_string('emails/contact_step_two_user.html', user_context)
        
        send_mail(
            subject=user_subject,
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contact.email],
            html_message=user_html_message,
            fail_silently=False,
        )
        
        logger.info(f"Contact emails sent successfully for {contact.email}")
        
    except Exception as e:
        logger.error(f"Failed to send contact emails: {str(e)}", exc_info=True)
        raise


@require_http_methods(["POST"])
def validate_email_ajax(request):
    """AJAX endpoint to validate email"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()
        else:
            email = request.POST.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({
                'valid': False,
                'message': str(_('Email is required.'))
            })
        
        # Check if email is already in database (optional)
        existing_contact = ContactStepTwo.objects.filter(email=email).first()
        if existing_contact:
            return JsonResponse({
                'valid': True,
                'message': str(_('This email has been used before.')),
                'warning': True
            })
        
        # Basic email validation
        from django.core.validators import EmailValidator
        validator = EmailValidator()
        try:
            validator(email)
            return JsonResponse({
                'valid': True,
                'message': str(_('Email is valid.'))
            })
        except:
            return JsonResponse({
                'valid': False,
                'message': str(_('Please enter a valid email address.'))
            })
            
    except Exception as e:
        logger.error(f"Email validation error: {str(e)}")
        return JsonResponse({
            'valid': False,
            'message': str(_('Error validating email.'))
        })