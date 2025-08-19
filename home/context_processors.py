from .models import Review, PageHeader, PartnerLogo, General
from product.models import Product
from django.urls import resolve

def page_header_context(request):
    try:
        current_slug = resolve(request.path_info).url_name
        header = PageHeader.objects.get(slug=current_slug)
    except:
        header = None
    return {'page_header': header}



def review_context(request):

    return {
        'approved_reviews': Review.objects.filter(is_approved=True).order_by('-approved_at')[:10],
        'review_count': Review.objects.filter(is_approved=True).count(),
    }


def featured_products_context(request):
    general = General.objects.last()
    return {
        'featured_products': Product.objects.filter(in_home=True).order_by('order'),
        'products_description':  general.products_description,
        'products_background': general.products_background.url,
    }

def partners_context(request):
    general = General.objects.last()
    return {
        'partner_logos':  PartnerLogo.objects.all(),
         'partners_description':  general.partners_description,
    }
