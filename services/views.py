from django.shortcuts import render
from .models import (
    Services,
    Service_Content
)

def service_view(request):
    services = Services.objects.filter(in_service_page=True).order_by('order')
    service_contents = Service_Content.objects.all() 
    context = {
        'services': services,
        'service_contents': service_contents,
    }
    
    return render(request, 'services.html', context)
