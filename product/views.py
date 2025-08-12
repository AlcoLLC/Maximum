from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Product_group, Segments, Oil_Types, Viscosity, ProductProperty
from django.http import JsonResponse
from home.models import PartnerLogo
import requests

from django.utils.translation import gettext as _
import logging
logger = logging.getLogger(__name__)

def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(product_id__icontains=search_query)
        )
    selected_product_groups = request.GET.getlist('product_group')
    if selected_product_groups:
        products = products.filter(product_group__slug__in=selected_product_groups)
    selected_segments = request.GET.getlist('segments')
    if selected_segments:
        products = products.filter(segments__slug__in=selected_segments)
    selected_oil_types = request.GET.getlist('oil_type')
    if selected_oil_types:
        products = products.filter(oil_type__slug__in=selected_oil_types)
    selected_viscosity = request.GET.getlist('viscosity')
    if selected_viscosity:
        products = products.filter(viscosity__slug__in=selected_viscosity)
    
    products = products.select_related('product_group').order_by('order', 'product_group__order').distinct()
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    product_groups = Product_group.objects.all().order_by('order')
    segments = Segments.objects.all()
    oil_types = Oil_Types.objects.all()
    viscosity_options = Viscosity.objects.all()
    partner_logos = PartnerLogo.objects.all()
    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'product_groups': product_groups,
        'segments': segments,
        'oil_types': oil_types,
        'viscosity_options': viscosity_options,
        'search_query': search_query,
        'selected_product_groups': selected_product_groups,
        'selected_segments': selected_segments,
        'selected_oil_types': selected_oil_types,
        'selected_viscosity': selected_viscosity,
        'partner_logos': partner_logos,
    }
    return render(request, 'product.html', context)

def product_detail(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        properties = ProductProperty.objects.filter(product=product).order_by('order', 'id')
        available_liters = product.liters.all().order_by('volume')

        related_products = Product.objects.filter(
            product_group=product.product_group
        ).exclude(
            id=product.id
        ).order_by('-id')[:3] 

        title = product.title or ""
        full_title = title
        if title and len(title) < 60:
            full_title = title + " " + _(" | MAXIMUM")

        description = product.description or ""
        if description and len(description) < 160:
            description += " " + (title or "")

        context = {
            'product': product,
            'available_liters': available_liters,
            'properties': properties,
            'meta_title': full_title[:60],
            'meta_description': description[:160],
            'related_products': related_products,  # Yeni əlavə edildi

        }

        return render(request, 'product_detail.html', context)
    
    except Exception as e:
        logger.error(f"[PRODUCT_DETAIL_ERROR] slug={slug} error={str(e)}", exc_info=True)
        return render(request, '500.html', status=500)

def product_properties_ajax(request, product_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = get_object_or_404(Product, id=product_id)
        properties = ProductProperty.objects.filter(product=product).order_by('order', 'id')

        properties_data = []
        for prop in properties:
            properties_data.append({
                'property_name': prop.property_name,
                'unit': prop.unit or '',
                'test_method': prop.test_method,
                'typical_value': prop.typical_value,
            })

        def check_url(url):
            if not url:
                return ''
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                response = requests.head(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    return url
            except requests.exceptions.RequestException:
                pass
            return ''

        pds_url = check_url(product.pds_url)
        sds_url = check_url(product.sds_url)
        tds_url = check_url(product.tds_url)

        return JsonResponse({
            'success': True,
            'properties': properties_data,
            'product_title': product.title,
            'pds_url': pds_url,
            'sds_url': sds_url,
            'tds_url': tds_url,
        })

    return JsonResponse({'success': False, 'error': 'Invalid request'})
