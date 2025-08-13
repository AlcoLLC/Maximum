from django.shortcuts import render
from .models import (
    Services,
    Service_Content
)

def service_view(request):
    services = Services.objects.all()
    service_contents = Service_Content.objects.all() 
    context = {
        'services': services,
        'service_contents': service_contents,
    }
    
    return render(request, 'services.html', context)
