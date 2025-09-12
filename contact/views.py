from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
import logging
import json
import requests

# Bu form sinfini öz forms.py faylınızdan import etməlisiniz
# Əgər yaratmamısınızsa, mütləq yaratmalısınız. Nümunəsi koddan sonra verilib.
from .forms import ContactStepTwoForm
from .models import ContactStepTwo, ContactInfo

# Logger konfiqurasiyası
logger = logging.getLogger(__name__)

# reCAPTCHA açarlarını settings-dən təhlükəsiz şəkildə alınması
RECAPTCHA_SITE_KEY = getattr(settings, 'RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = getattr(settings, 'RECAPTCHA_SECRET_KEY', '')


def get_client_ip(request):
    """Müştərinin IP ünvanını sorğudan əldə edir."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def verify_recaptcha(recaptcha_response, client_ip=None):
    """reCAPTCHA cavabını təkmilləşdirilmiş yoxlama ilə təsdiqləyir."""
    if not recaptcha_response:
        logger.warning("Boş reCAPTCHA cavabı alındı.")
        return False
    if not RECAPTCHA_SECRET_KEY:
        logger.error("RECAPTCHA_SECRET_KEY təyin edilməyib.")
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
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        logger.debug(f"reCAPTCHA yoxlama nəticəsi: {result}")

        if not result.get('success', False):
            error_codes = result.get('error-codes', [])
            logger.warning(f"reCAPTCHA təsdiqlənmədi. Xəta kodları: {error_codes}")
            return False
        
        logger.info("reCAPTCHA uğurla təsdiqləndi.")
        return True

    except requests.RequestException as e:
        logger.error(f"reCAPTCHA yoxlama zamanı şəbəkə xətası: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"reCAPTCHA yoxlama zamanı gözlənilməz xəta: {str(e)}", exc_info=True)
        return False


def contact_step_two_view(request):
    """Əsas əlaqə formu view-su (düzəldilmiş və tamamlanmış)."""
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
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # 1. reCAPTCHA yoxlanması
        recaptcha_response = request.POST.get('g-recaptcha-response')
        client_ip = get_client_ip(request)
        
        if not verify_recaptcha(recaptcha_response, client_ip):
            error_message = _("reCAPTCHA verification failed. Please try again.")
            logger.warning(f"reCAPTCHA təsdiqlənmədi. IP: {client_ip}")
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message, 'recaptcha_failed': True}, status=400)
            else:
                messages.error(request, error_message)
                return redirect('contact:contact_step_two')

        # 2. IP limitinin yoxlanması
        if client_ip:
            submission_count = ContactStepTwo.objects.filter(ip_address=client_ip).count()
            if submission_count >= 5:
                error_message = _("Maximum number of submissions reached from this IP address.")
                logger.warning(f"IP limiti aşıldı ({submission_count} müraciət). IP: {client_ip}")
                if is_ajax:
                    return JsonResponse({'success': False, 'message': error_message}, status=429) # 429 - Too Many Requests
                else:
                    messages.error(request, error_message)
                    return redirect('contact:contact_step_two')
        
        # 3. Formun validasiyası və saxlanması (əlavə edilmiş əsas məntiq)
        form = ContactStepTwoForm(request.POST)
        if form.is_valid():
            try:
                contact_instance = form.save(commit=False)
                contact_instance.ip_address = client_ip
                contact_instance.save()
                
                logger.info(f"Yeni müraciət uğurla saxlandı: {contact_instance.email}")

                # E-poçtları göndərmək üçün köməkçi funksiyanı çağırırıq
                send_contact_emails(contact_instance)
                
                success_message = _("Your message has been sent successfully. Thank you for contacting us!")
                if is_ajax:
                    return JsonResponse({'success': True, 'message': success_message})
                else:
                    messages.success(request, success_message)
                    return redirect('/')  # Uğurlu halda ana səhifəyə yönləndir
            
            except Exception as e:
                logger.error(f"Formun işlənməsi və ya e-poçt göndərilməsi zamanı xəta: {str(e)}", exc_info=True)
                error_message = _("An error occurred. Please try again or contact us directly.")
                if is_ajax:
                    return JsonResponse({'success': False, 'message': error_message}, status=500)
                else:
                    messages.error(request, error_message)
                    return redirect('contact:contact_step_two')
        else:
            # Form etibarsız olduqda
            logger.warning(f"Form validasiya xətaları: {form.errors.as_json()}")
            if is_ajax:
                return JsonResponse({'success': False, 'message': _("Please correct the errors below."), 'errors': form.errors}, status=400)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields.get(field).label if form.fields.get(field) else field.replace('_', ' ').title()}: {error}")
                return redirect('contact:contact_step_two')

    # GET sorğusu üçün formanı və məlumatları hazırlayırıq
    contact_info = ContactInfo.objects.last()
    context = {
        'role_choices': ContactStepTwo.ROLE_CHOICES,
        'question_type_choices': ContactStepTwo.QUESTION_TYPE_CHOICES,
        'contact_info': contact_info,
        'form_labels': form_labels,
        'recaptcha_site_key': RECAPTCHA_SITE_KEY,
        'form': ContactStepTwoForm() # GET sorğusu üçün boş form
    }
    return render(request, 'contact_step_two.html', context)


def send_contact_emails(contact):
    """Həm adminə, həm də istifadəçiyə təsdiq e-poçtu göndərir."""
    logger.info(f"E-poçt göndərmə prosesi başlayır: {contact.email}")
    try:
        # Adminə bildiriş e-poçtu
        admin_subject = f"New Contact Form Submission - {contact.first_name} {contact.last_name}"
        admin_html_message = render_to_string('emails/contact_step_two_admin.html', {'contact': contact})
        admin_emails = getattr(settings, 'CONTACT_EMAIL', ['info@maximumlube.com']) # Emaili settings-dən götürün
        
        send_mail(
            subject=admin_subject,
            message='', # HTML istifadə etdiyimiz üçün boş saxlaya bilərik
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails if isinstance(admin_emails, list) else [admin_emails],
            html_message=admin_html_message,
            fail_silently=False
        )
        logger.info(f"Admin bildirişi uğurla göndərildi: {', '.join(admin_emails)}")

        # İstifadəçiyə təsdiq e-poçtu
        user_subject = _("Thank you for contacting Maximum")
        user_html_message = render_to_string('emails/contact_step_two_user.html', {'contact': contact})
        
        send_mail(
            subject=user_subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            html_message=user_html_message,
            fail_silently=False
        )
        logger.info(f"İstifadəçi təsdiq e-poçtu uğurla göndərildi: {contact.email}")
    except Exception as e:
        # Xətanı loglayırıq, ancaq proqramın dayanmasının qarşısını alırıq
        logger.error(f"E-poçt göndərilərkən xəta baş verdi: {str(e)}", exc_info=True)
        # İstəsəniz burada xətanı yenidən "raise" edə bilərsiniz, amma bu, istifadəçinin uğur mesajı almasına mane ola bilər
        # raise e 


@require_http_methods(["POST"])
def validate_email_ajax(request):
    """E-poçtun AJAX vasitəsilə yoxlanılması."""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'valid': False, 'message': _('Invalid request.')}, status=400)
    
    from django.core.validators import validate_email, ValidationError
    try:
        validate_email(email)
        # E-poçtun daha əvvəl istifadə edilib-edilmədiyini yoxlaya bilərik
        if ContactStepTwo.objects.filter(email=email).exists():
            return JsonResponse({'valid': True, 'warning': True, 'message': _('This email has been used before.')})
        return JsonResponse({'valid': True, 'message': _('Email is valid.')})
    except ValidationError:
        return JsonResponse({'valid': False, 'message': _('Please enter a valid email address.')})


def contact_info_view(request):
    """Sadəcə əlaqə məlumatlarını göstərən view."""
    contact_info = ContactInfo.objects.last()
    context = {'contact_info': contact_info}
    return render(request, 'contact.html', context)