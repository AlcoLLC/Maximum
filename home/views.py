from django.shortcuts import render, redirect
from .models import HomeSwiper, Review, General
from product.models import Product_group
from news.models import News
from faq.models import FAQ
from services.models import Services
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import timedelta

# Create your views here.


def home_view(request): 
    swiper_images = HomeSwiper.objects.filter(is_active=True).order_by('order')
    product_groups_sec1 = Product_group.objects.filter(in_home_sec1=True).order_by('order')  
    product_groups_sec2 = Product_group.objects.filter(in_home_sec2=True).order_by('order')  
    latest_news = News.objects.filter(in_home=True)
    home_faqs = FAQ.objects.filter(in_home=True)[:4]
    services = Services.objects.all()
    general = General.objects.last()

    context = { 
        'swiper_images': swiper_images,
        'product_groups_sec1': product_groups_sec1,
        'product_groups_sec2': product_groups_sec2,
        'latest_news': latest_news,
        'home_faqs': home_faqs,
        'services': services,
        'general': general,
    } 
     
    return render(request, 'home.html', context)

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_protect
@require_POST
def submit_review(request):
    """Handle review submission for all pages"""
    try:
        # Get form data
        rating_value = request.POST.get('rating')
        first_name = request.POST.get('first_name', '').strip()
        surname = request.POST.get('surname', '').strip()
        email_address = request.POST.get('email_address', '').strip()
        summary = request.POST.get('summary', '').strip()
        review_text = request.POST.get('review', '').strip()
        agreement = request.POST.get('agreement')
        
        # Get the page user came from
        redirect_url = request.POST.get('redirect_url', '/')
        
        # Basic validations
        if not rating_value:
            messages.error(request, _('Please select a rating.'))
            return redirect(redirect_url)
            
        if not agreement:
            messages.error(request, _('You must accept the agreement terms.'))
            return redirect(redirect_url)
        
        # Check required fields
        required_fields = {
            'first_name': first_name,
            'surname': surname,
            'email_address': email_address,
            'summary': summary,
            'review': review_text
        }
        
        for field_name, field_value in required_fields.items():
            if not field_value:
                messages.error(request, _('All fields are required.'))
                return redirect(redirect_url)

        # Spam check - same email in last 24 hours?
        recent_review = Review.objects.filter(
            email_address=email_address,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).first()
        
        if recent_review:
            messages.error(request, _('You have already submitted a review in the last 24 hours. Please wait.'))
            return redirect(redirect_url)

        # Create review
        review = Review(
            first_name=first_name,
            surname=surname,
            email_address=email_address,
            summary=summary,
            review=review_text,
            rating=int(rating_value),
            ip_address=get_client_ip(request),
            is_approved=False
        )
        
        review.full_clean()
        review.save()
        
        messages.success(request, _('Your review has been submitted successfully. Thank you for your valuable feedback!'))
        return redirect(redirect_url)
        
    except ValueError:
        messages.error(request, _('Invalid rating value. Please select a rating.'))
        return redirect(redirect_url)
    except ValidationError as e:
        error_message = ', '.join([str(error) for error in e.messages])
        messages.error(request, f'Validation error: {error_message}')
        return redirect(redirect_url)
    except Exception as e:
        messages.error(request, _('An error occurred while submitting your review. Please try again.'))
        return redirect(redirect_url)

# Error handlers
def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler500(request):
    return render(request, '500.html', status=500)

def handler503(request, exception):
    return render(request, '503.html', status=503)