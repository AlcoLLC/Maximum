from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
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
                'url': f'/product/{product.slug}/',
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
                'url': f'/product-group/{group.slug}/',
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
                'url': f'/segment/{segment.slug}/',
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
                'url': f'/oil-type/{oil_type.slug}/',
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
                'url': f'/viscosity/{viscosity.slug}/',
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
                'url': f'/product/{prop.product.slug}/',
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
                'url': '/#reviews',
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
                'url': f'/about/{about.id}/',
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
                'url': f'/about/{content.about.id}/',
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
                'url': f'/about/{section.about.id}/',
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
                'url': f'/global-presence/{presence.id}/',
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
                'url': f'/sustainability/{sustainability.id}/',
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
                'url': f'/partnership/{partnership.id}/',
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
                'url': f'/partnership/{content.id}/',
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
                'url': f'/brand/guideline/{guideline.id}/',
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
                'url': f'/brand/promo-library/{library.id}/',
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
                'url': f'/brand/promo-material/{material.id}/',
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
                'url': f'/brand/image-library/{library.id}/',
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
                'url': f'/brand/video-library/{library.id}/',
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
                'url': f'/news/{news.slug}/',
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
                    'url': f'/news/{content.news.slug}/',
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
                'url': f'/services/{service.id}/',
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
                'url': f'/service-content/{content.id}/',
                'type': 'Service Content',
                'image': content.image.url if content.image else None
            })

        # FAQ search
        faq_fields = ['question', 'answer']
        faqs = FAQ.objects.filter(
            build_search_q(query, faq_fields),
            is_active=True
        ).distinct()
        
        for faq in faqs:
            results.append({
                'title': faq.question,
                'description': faq.answer[:200] + '...' if faq.answer and len(faq.answer) > 200 else faq.answer or '',
                'url': '/faq/',
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