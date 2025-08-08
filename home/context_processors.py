from .models import Review, PageHeader
from django.urls import resolve

def page_header_context(request):
    try:
        current_slug = resolve(request.path_info).url_name
        header = PageHeader.objects.get(slug=current_slug)
    except:
        header = None
    return {'page_header': header}



def review_context(request):
    """
    Global context processor for reviews
    This will be available in all templates
    """
    return {
        'approved_reviews': Review.objects.filter(is_approved=True).order_by('-approved_at')[:10],
        'review_count': Review.objects.filter(is_approved=True).count(),
    }
