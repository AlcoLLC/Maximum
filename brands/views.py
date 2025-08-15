from django.shortcuts import render

# Create your views here.

def brand_view(request):
    context = {
    }
    
    return render(request, 'brand_portal.html', context)