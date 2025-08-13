from django.shortcuts import render
from .models import (
    Partnership_Content
)

def service_view(request):
    partnership_contents = Partnership_Content.objects.all() 
    context = {
        'partnership_contents': partnership_contents,
    }
    
    return render(request, 'partnership.html', context)
