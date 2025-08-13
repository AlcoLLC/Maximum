from django.shortcuts import render
# from .models import (
#     Service,
#     Service_Content,
#     ServiceHighlight
# )



def service_view(request):

    context = {

    }
    
    return render(request, 'services.html', context)
