from django.shortcuts import render
from .models import (
    BrandGuidelineDocument,
    PromoMaterialsLibrary,
    BrandImageLibrary,
    BrandVideoLibrary
)

def brand_view(request, tab=None):
    valid_tabs = ['brand-guideline', 'promo-materials', 'image-library', 'videos']
    active_tab = tab if tab in valid_tabs else None
    
    guideline = BrandGuidelineDocument.objects.last()
    promo_material = PromoMaterialsLibrary.objects.prefetch_related('promo_materials').last()
    image_library = BrandImageLibrary.objects.prefetch_related('images').last()
    video_library = BrandVideoLibrary.objects.prefetch_related('videos').last()

    context = {
        'guideline': guideline,
        'promo_material': promo_material,
        'image_library': image_library,
        'video_library': video_library,
        'active_tab': active_tab,
    }
    
    return render(request, 'brand_portal.html', context)