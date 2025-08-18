from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.translation import get_language
from home.models import Review
from product.models import Product, Product_group, ProductProperty, Segments, Oil_Types, Viscosity
from brands.models import BrandGuidelineDocument, BrandImageLibrary, BrandVideoLibrary, PromoMaterial, PromoMaterialsLibrary
from about.models import About, AboutContent, AboutSection, GlobalPresence, Sustainability, PartnershipContent
from news.models import News, News_Content
from faq.models import FAQ
from services.models import Services, Service_Content
from partnership.models import Partnership_Content


def create_search_queries(query):
    """
    Create multiple search queries from the input:
    1. Full query
    2. Individual words
    3. Partial matches for each word
    """
    queries = []
    queries.append(query.strip())
    words = [word.strip() for word in query.split() if len(word.strip()) >= 2]
    queries.extend(words)
    
    return queries

def build_search_q(query, fields):
    """
    Build a Q object for searching across multiple fields with partial matching
    """
    q_objects = Q()
    search_queries = create_search_queries(query)
    
    for field in fields:
        for search_term in search_queries:
            q_objects |= Q(**{f"{field}__icontains": search_term})
    
    return q_objects

def get_localized_url(url_name, args=None, kwargs=None):
    """
    Get URL with current language prefix
    """
    current_language = get_language()
    
    try:
        if args:
            url = reverse(url_name, args=args)
        elif kwargs:
            url = reverse(url_name, kwargs=kwargs)
        else:
            url = reverse(url_name)
    except:
        # Fallback to manual URL construction if reverse fails
        if args:
            url = f"/{'/'.join(str(arg) for arg in args)}/"
        else:
            url = "/"
    
    # If current language is not default (en) and URL doesn't start with language prefix
    if current_language != 'en' and not url.startswith(f'/{current_language}/'):
        url = f'/{current_language}{url}'
    
    return url


def search_view(request):
    query = request.GET.get('search', '').strip()
    results = []
    total_results = 0

    if query and len(query) >= 2:  

        # Product search
        product_fields = ['title', 'description', 'features_benefits', 'application', 
                         'recommendations', 'product_id', 'api', 'ilsac', 'acea', 'jaso', 'oem_sertification']
        
        products = Product.objects.filter(
            build_search_q(query, product_fields)
        ).distinct()
        
        for product in products:
            results.append({
                'title': product.title,
                'description': product.description[:200] + '...' if product.description and len(product.description) > 200 else product.description or '',
                'url': get_localized_url('product:product_detail', kwargs={'slug': product.slug}),
                'type': 'Product',
                'image': product.image.url if product.image else None
            })

        # Product Group search
        product_group_fields = ['title', 'description']
        product_groups = Product_group.objects.filter(
            build_search_q(query, product_group_fields)
        ).distinct()
        
        for group in product_groups:
            results.append({
                'title': group.title,
                'description': group.description[:200] + '...' if group.description and len(group.description) > 200 else group.description or '',
                'url': get_localized_url('product:product_group_detail', kwargs={'slug': group.slug}),
                'type': 'Product Group',
                'image': group.image.url if group.image else None
            })

        # Segments search
        segments = Segments.objects.filter(
            build_search_q(query, ['title'])
        ).distinct()
        
        for segment in segments:
            results.append({
                'title': segment.title,
                'description': f'Segment: {segment.title}',
                'url': get_localized_url('product:segment_detail', kwargs={'slug': segment.slug}),
                'type': 'Segment',
                'image': None
            })

        # Oil Types search
        oil_types = Oil_Types.objects.filter(
            build_search_q(query, ['title'])
        ).distinct()
        
        for oil_type in oil_types:
            results.append({
                'title': oil_type.title,
                'description': f'Oil Type: {oil_type.title}',
                'url': get_localized_url('product:oil_type_detail', kwargs={'slug': oil_type.slug}),
                'type': 'Oil Type',
                'image': None
            })

        # Viscosity search
        viscosities = Viscosity.objects.filter(
            build_search_q(query, ['title'])
        ).distinct()
        
        for viscosity in viscosities:
            results.append({
                'title': viscosity.title,
                'description': f'Viscosity: {viscosity.title}',
                'url': get_localized_url('product:viscosity_detail', kwargs={'slug': viscosity.slug}),
                'type': 'Viscosity',
                'image': None
            })

        # Product Properties search
        product_properties = ProductProperty.objects.filter(
            build_search_q(query, ['property_name', 'test_method', 'typical_value'])
        ).select_related('product').distinct()
        
        for prop in product_properties:
            results.append({
                'title': f'{prop.product.title} - {prop.property_name}',
                'description': f'Property: {prop.property_name}, Test Method: {prop.test_method}, Value: {prop.typical_value}',
                'url': get_localized_url('product:product_detail', kwargs={'slug': prop.product.slug}),
                'type': 'Product Property',
                'image': prop.product.image.url if prop.product.image else None
            })

        # Reviews search
        review_fields = ['first_name', 'surname', 'summary', 'review']
        reviews = Review.objects.filter(
            build_search_q(query, review_fields),
            is_approved=True
        ).distinct()
        
        for review in reviews:
            results.append({
                'title': f'Review by {review.full_name} - {review.rating}★',
                'description': review.summary if review.summary else review.review[:200] + '...' if len(review.review) > 200 else review.review,
                'url': get_localized_url('home:home') + '#reviews',
                'type': 'Review',
                'image': None
            })

        # About search
        about_fields = ['title', 'content']
        abouts = About.objects.filter(
            build_search_q(query, about_fields)
        ).distinct()
        
        for about in abouts:
            results.append({
                'title': about.title,
                'description': about.content[:200] + '...' if about.content and len(about.content) > 200 else about.content or '',
                'url': get_localized_url('about:about_detail', kwargs={'pk': about.id}),
                'type': 'About',
                'image': None
            })

        # About Content search
        about_content_fields = ['section_title', 'section_content']
        about_contents = AboutContent.objects.filter(
            build_search_q(query, about_content_fields)
        ).select_related('about').distinct()
        
        for content in about_contents:
            results.append({
                'title': content.section_title,
                'description': content.section_content[:200] + '...' if content.section_content and len(content.section_content) > 200 else content.section_content or '',
                'url': get_localized_url('about:about_detail', kwargs={'pk': content.about.id}),
                'type': 'About Section',
                'image': content.image.url if content.image else None
            })

        # About Section search
        about_section_fields = ['section_title', 'section_description', 'category']
        about_sections = AboutSection.objects.filter(
            build_search_q(query, about_section_fields)
        ).select_related('about').distinct()
        
        for section in about_sections:
            results.append({
                'title': section.section_title,
                'description': section.section_description[:200] + '...' if section.section_description and len(section.section_description) > 200 else section.section_description or '',
                'url': get_localized_url('about:about_detail', kwargs={'pk': section.about.id}),
                'type': 'About Section',
                'image': section.image.url if section.image else None
            })

        # Global Presence search
        global_presence_fields = ['title', 'description_one', 'description_two', 'description_three']
        global_presences = GlobalPresence.objects.filter(
            build_search_q(query, global_presence_fields)
        ).distinct()
        
        for presence in global_presences:
            results.append({
                'title': presence.title,
                'description': presence.description_one[:200] + '...' if presence.description_one and len(presence.description_one) > 200 else presence.description_one or '',
                'url': get_localized_url('about:global_presence_detail', kwargs={'pk': presence.id}),
                'type': 'Global Presence',
                'image': None
            })

        # Sustainability search
        sustainability_fields = ['title', 'description']
        sustainabilities = Sustainability.objects.filter(
            build_search_q(query, sustainability_fields)
        ).distinct()
        
        for sustainability in sustainabilities:
            results.append({
                'title': sustainability.title,
                'description': sustainability.description[:200] + '...' if sustainability.description and len(sustainability.description) > 200 else sustainability.description or '',
                'url': get_localized_url('about:sustainability_detail', kwargs={'pk': sustainability.id}),
                'type': 'Sustainability',
                'image': sustainability.image.url if sustainability.image else None
            })

        # Partnership Content search
        partnership_fields = ['title', 'title_content', 'description']
        partnerships = PartnershipContent.objects.filter(
            build_search_q(query, partnership_fields)
        ).distinct()
        
        for partnership in partnerships:
            results.append({
                'title': partnership.title,
                'description': partnership.description[:200] + '...' if partnership.description and len(partnership.description) > 200 else partnership.description or '',
                'url': get_localized_url('partnership:partnership_detail', kwargs={'pk': partnership.id}),
                'type': 'Partnership',
                'image': partnership.image.url if partnership.image else None
            })

        # Partnership Content search (new model)
        partnership_content_fields = ['subtitle', 'title', 'description']
        partnership_contents = Partnership_Content.objects.filter(
            build_search_q(query, partnership_content_fields)
        ).distinct()
        
        for content in partnership_contents:
            results.append({
                'title': content.title,
                'description': content.description[:200] + '...' if content.description and len(content.description) > 200 else content.description or '',
                'url': get_localized_url('partnership:partnership_content_detail', kwargs={'pk': content.id}),
                'type': 'Partnership Content',
                'image': content.image.url if content.image else None
            })

        # Brand Guideline Document search
        brand_guideline_fields = ['title', 'short_content', 'description']
        brand_guidelines = BrandGuidelineDocument.objects.filter(
            build_search_q(query, brand_guideline_fields)
        ).distinct()
        
        for guideline in brand_guidelines:
            results.append({
                'title': guideline.title,
                'description': guideline.short_content,
                'url': get_localized_url('brands:guideline_detail', kwargs={'pk': guideline.id}),
                'type': 'Brand Guideline',
                'image': guideline.preview_image.url if guideline.preview_image else None
            })

        # Promo Materials Library search
        promo_library_fields = ['short_content', 'description']
        promo_libraries = PromoMaterialsLibrary.objects.filter(
            build_search_q(query, promo_library_fields)
        ).distinct()
        
        for library in promo_libraries:
            results.append({
                'title': library.short_content,
                'description': library.description[:200] + '...' if library.description and len(library.description) > 200 else library.description or '',
                'url': get_localized_url('brands:promo_library_detail', kwargs={'pk': library.id}),
                'type': 'Promo Materials Library',
                'image': None
            })

        # Promo Material search
        promo_material_fields = ['title']
        promo_materials = PromoMaterial.objects.filter(
            build_search_q(query, promo_material_fields)
        ).select_related('library').distinct()
        
        for material in promo_materials:
            results.append({
                'title': material.title,
                'description': material.library.short_content,
                'url': get_localized_url('brands:promo_material_detail', kwargs={'pk': material.id}),
                'type': 'Promo Material',
                'image': material.preview_image.url if material.preview_image else None
            })

        # Brand Image Library search
        brand_image_library_fields = ['short_content', 'description']
        brand_image_libraries = BrandImageLibrary.objects.filter(
            build_search_q(query, brand_image_library_fields)
        ).distinct()
        
        for library in brand_image_libraries:
            results.append({
                'title': library.short_content,
                'description': library.description[:200] + '...' if library.description and len(library.description) > 200 else library.description or '',
                'url': get_localized_url('brands:image_library_detail', kwargs={'pk': library.id}),
                'type': 'Brand Image Library',
                'image': None
            })

        # Brand Video Library search
        brand_video_library_fields = ['short_content', 'description']
        brand_video_libraries = BrandVideoLibrary.objects.filter(
            build_search_q(query, brand_video_library_fields)
        ).distinct()
        
        for library in brand_video_libraries:
            results.append({
                'title': library.short_content,
                'description': library.description[:200] + '...' if library.description and len(library.description) > 200 else library.description or '',
                'url': get_localized_url('brands:video_library_detail', kwargs={'pk': library.id}),
                'type': 'Brand Video Library',
                'image': None
            })

        # News search
        news_fields = ['title', 'content']
        news_items = News.objects.filter(
            build_search_q(query, news_fields),
            is_active=True
        ).distinct()
        
        for news in news_items:
            results.append({
                'title': news.title,
                'description': news.content[:200] + '...' if news.content and len(news.content) > 200 else news.content or '',
                'url': get_localized_url('news:news_detail', kwargs={'slug': news.slug}),
                'type': 'News',
                'image': news.image.url if news.image else None
            })

        # News Content search
        news_content_fields = ['description']
        news_contents = News_Content.objects.filter(
            build_search_q(query, news_content_fields)
        ).select_related('news').distinct()
        
        for content in news_contents:
            if content.news.is_active:
                results.append({
                    'title': content.news.title,
                    'description': content.description[:200] + '...' if content.description and len(content.description) > 200 else content.description or '',
                    'url': get_localized_url('news:news_detail', kwargs={'slug': content.news.slug}),
                    'type': 'News Content',
                    'image': content.image.url if content.image else content.news.image.url if content.news.image else None
                })

        # Services search
        services_fields = ['title', 'description']
        services = Services.objects.filter(
            build_search_q(query, services_fields)
        ).distinct()
        
        for service in services:
            results.append({
                'title': service.title,
                'description': service.description[:200] + '...' if service.description and len(service.description) > 200 else service.description or '',
                'url': get_localized_url('services:service_detail', kwargs={'pk': service.id}),
                'type': 'Service',
                'image': service.image.url if service.image else None
            })

        # Service Content search
        service_content_fields = ['subtitle', 'title', 'description']
        service_contents = Service_Content.objects.filter(
            build_search_q(query, service_content_fields)
        ).distinct()
        
        for content in service_contents:
            results.append({
                'title': content.title,
                'description': content.description[:200] + '...' if content.description and len(content.description) > 200 else content.description or '',
                'url': get_localized_url('services:service_content_detail', kwargs={'pk': content.id}),
                'type': 'Service Content',
                'image': content.image.url if content.image else None
            })

        # FA Qsearch
        faq_fields = ['question', 'answer']
        faqs = FAQ.objects.filter(
            build_search_q(query, faq_fields),
            is_active=True
        ).distinct()
        
        for faq in faqs:
            results.append({
                'title': faq.question,
                'description': faq.answer[:200] + '...' if faq.answer and len(faq.answer) > 200 else faq.answer or '',
                'url': get_localized_url('faq:faq'),
                'type': 'FAQ',
                'image': None
            })

        # Remove duplicates
        seen = set()
        unique_results = []
        for result in results:
            identifier = (result['title'], result['type'])
            if identifier not in seen:
                seen.add(identifier)
                unique_results.append(result)
        
        results = unique_results
        total_results = len(results)
        
        # Calculate relevance and sort
        def calculate_relevance(result):
            title_lower = result['title'].lower()
            desc_lower = result['description'].lower()
            query_lower = query.lower()
            
            if query_lower in title_lower:
                return 100
            elif query_lower in desc_lower:
                return 80
            else:
                score = 0
                for word in query_lower.split():
                    if word in title_lower:
                        score += 20
                    elif word in desc_lower:
                        score += 10
                return score
        
        results.sort(key=calculate_relevance, reverse=True)
        
        # Pagination
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None

    context = {
        'query': query,
        'results': page_obj,
        'total_results': total_results,
    }
    
    return render(request, 'search.html', context)