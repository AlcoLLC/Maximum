# contact/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from .models import ContactStepTwo
from .forms import ContactStepTwoForm 
import logging
import json
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def contact_step_two_view(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        client_ip = get_client_ip(request)
        time_threshold = timezone.now() - timedelta(hours=1)
        recent_submissions_count = ContactStepTwo.objects.filter(
            ip_address=client_ip,
            created_at__gte=time_threshold
        ).count()
        
        SUBMISSION_LIMIT = 3 
        if recent_submissions_count >= SUBMISSION_LIMIT:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            message = _('You have made too many submissions recently. Please try again later.')
            return JsonResponse({'success': False, 'message': message}, status=429)

        try:
            if is_ajax and request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': _('Invalid JSON data.')}, status=400)

        form = ContactStepTwoForm(data)
        
        if form.is_valid():
            contact = form.save(commit=False)
            contact.ip_address = client_ip
            contact.save()
            
            try:
                send_contact_emails(contact)
                logger.info(f"Contact form submitted and emails sent successfully for {contact.email}")
                message = _('Thank you for contacting us! We will get back to you soon.')
                if not is_ajax:
                    messages.success(request, message)
                    return redirect('contact:contact_step_two')
                return JsonResponse({'success': True, 'message': str(message)})
            
            except Exception as e:
                logger.error(f"Error sending contact emails for {contact.email}: {str(e)}", exc_info=True)
                message = _('Your message was saved, but we encountered an error sending emails. We will still get back to you.')
                if not is_ajax:
                    messages.warning(request, message)
                    return redirect('contact:contact_step_two')
                return JsonResponse({'success': True, 'message': str(message)})

        else:  
            logger.warning(f"Form validation failed: {form.errors}")
            if not is_ajax:
                context = {'form': form}
                return render(request, 'contact_step_two.html', context, status=400)
            
            return JsonResponse({
                'success': False,
                'errors': form.errors,
                'message': _('Please correct the errors below.')
            }, status=400)

    form = ContactStepTwoForm()
    context = {'form': form}
    return render(request, 'contact_step_two.html', context)

def contact_view(request):
    return render(request, 'contact.html')

def send_contact_emails(contact):
    """Send both admin notification and user confirmation emails"""
    
    # Debug logging
    logger.info(f"Starting email send process for contact: {contact.email}")
    logger.info(f"Email settings - HOST: {settings.EMAIL_HOST}, PORT: {settings.EMAIL_PORT}")
    logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    logger.info(f"CONTACT_EMAIL setting: {getattr(settings, 'CONTACT_EMAIL', 'Not set')}")
    
    # 1. Admin notification email
    try:
        admin_subject = f"New Contact Form Submission - {contact.first_name} {contact.last_name}"
        admin_context = {
            'contact': contact,
            'role_display': contact.get_role_display() if contact.role else 'Not specified',
            'question_type_display': contact.get_question_type_display() if contact.question_type else 'Not specified',
        }
        
        logger.info(f"Rendering admin email template with context: {admin_context}")
        admin_html_message = render_to_string('emails/contact_step_two_admin.html', admin_context)
        
        # FIXED: Remove list brackets around from_email
        # FIXED: Handle CONTACT_EMAIL properly
        admin_email = getattr(settings, 'CONTACT_EMAIL', 'aytacmehdizade08@gmail.com')
        if isinstance(admin_email, list):
            admin_email_list = admin_email
        else:
            admin_email_list = [admin_email]
            
        logger.info(f"Sending admin email to: {admin_email_list}")
        
        send_mail(
            subject=admin_subject,
            message='',  # Plain text fallback
            from_email=settings.EMAIL_HOST_USER,  # FIXED: Use settings directly
            recipient_list=admin_email_list,  # FIXED: Proper list format
            html_message=admin_html_message,
            fail_silently=False,
        )
        logger.info(f"Admin notification email sent successfully for {contact.email}")
        
    except Exception as e:
        logger.error(f"Failed to send admin notification email: {str(e)}", exc_info=True)
        raise
    
    # 2. User confirmation email
    try:
        user_subject = _("Thank you for contacting us - Tomoil")
        user_context = {
            'contact': contact,
            'role_display': contact.get_role_display() if contact.role else 'Not specified',
            'question_type_display': contact.get_question_type_display() if contact.question_type else 'Not specified',
        }
        
        logger.info(f"Rendering user email template with context: {user_context}")
        user_html_message = render_to_string('emails/contact_step_two_user.html', user_context)
        
        logger.info(f"Sending user confirmation email to: {contact.email}")
        
        send_mail(
            subject=user_subject,
            message='',  # Plain text fallback
            from_email=settings.EMAIL_HOST_USER,  # FIXED: Use settings directly
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
            return JsonResponse({'valid': True, 'warning': True, 'message': _('This email has been used before.')})
        return JsonResponse({'valid': True, 'message': _('Email is valid.')})
    except ValidationError:
        return JsonResponse({'valid': False, 'message': _('Please enter a valid email address.')})