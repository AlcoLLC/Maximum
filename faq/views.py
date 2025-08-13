from django.shortcuts import render
from .models import FAQ

def faq_view(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('created_at')
    

    context = {
        'faqs': faqs,
    }
    
    return render(request, 'faq.html', context)