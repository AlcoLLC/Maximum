from django.shortcuts import render
from .models import HomeSwiper, PartnerLogo

# Create your views here.


def home_view(request): 
    swiper_images = HomeSwiper.objects.filter(is_active=True).order_by('order')
    partner_logos = PartnerLogo.objects.all()
  
    context = { 
        'swiper_images': swiper_images,
        'partner_logos': partner_logos,

    } 
     
    return render(request, 'home.html', context)

# Error handlers
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler400(request, exception):
    return render(request, '400.html', status=400)