from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse, NoReverseMatch

# Bütün lazımi modelləri import edirik
from product.models import Product, Product_group, Segments, Oil_Types, Viscosity, ProductProperty
from brands.models import BrandGuidelineDocument, BrandImageLibrary, BrandVideoLibrary, PromoMaterial, PromoMaterialsLibrary
from about.models import About, AboutContent, AboutSection, GlobalPresence, Sustainability
from partnership.models import Partnership_Content
from news.models import News
from faq.models import FAQ
from services.models import Services, Service_Content
from home.models import Review

def create_search_queries(query):
    queries = []
    if query:
        queries.append(query.strip())
        words = [word.strip() for word in query.split() if len(word.strip()) >= 2]
        queries.extend(words)
    return list(set(queries))

def build_search_q(query, fields):
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
        product_fields = ['title', 'description', 'features_benefits', 'application', 'recommendations', 'product_id', 'api', 'ilsac', 'acea', 'jaso', 'oem_sertification']
        products = Product.objects.filter(build_search_q(query, product_fields)).distinct()
        for item in products:
            try:
                results.append({
                    'title': item.title,
                    'description': item.description,
                    'url': reverse('product:product_detail', kwargs={'slug': item.slug}),
                    'type': 'Product',
                    'image': item.image.url if item.image else None
                })
            except NoReverseMatch:
                continue

        # Product Group, Segments, etc. search (links to filtered product list)
        product_related_models = {
            'Product Group': (Product_group, ['title', 'description'], 'product_group'),
            'Segment': (Segments, ['title'], 'segments'),
            'Oil Type': (Oil_Types, ['title'], 'oil_type'),
            'Viscosity': (Viscosity, ['title'], 'viscosity'),
        }
        for type_name, (model, fields, query_param) in product_related_models.items():
            items = model.objects.filter(build_search_q(query, fields)).distinct()
            for item in items:
                try:
                    url = f"{reverse('product:products')}?{query_param}={item.slug}"
                    results.append({
                        'title': item.title,
                        'description': getattr(item, 'description', f'{type_name}: {item.title}'),
                        'url': url,
                        'type': type_name,
                        'image': getattr(item, 'image', None) and item.image.url
                    })
                except NoReverseMatch:
                    continue

        # Product Properties search (links to parent product)
        properties = ProductProperty.objects.filter(build_search_q(query, ['property_name', 'test_method', 'typical_value'])).select_related('product').distinct()
        for item in properties:
            try:
                results.append({
                    'title': f'{item.product.title} - {item.property_name}',
                    'description': f'Property: {item.property_name}, Test Method: {item.test_method}, Value: {item.typical_value}',
                    'url': reverse('product:product_detail', kwargs={'slug': item.product.slug}),
                    'type': 'Product Property',
                    'image': item.product.image.url if item.product.image else None
                })
            except NoReverseMatch:
                continue
        
        # News search
        news_items = News.objects.filter(build_search_q(query, ['title', 'content']), is_active=True).distinct()
        for item in news_items:
            try:
                results.append({
                    'title': item.title,
                    'description': item.content,
                    'url': reverse('news:news_detail', kwargs={'slug': item.slug}),
                    'type': 'News',
                    'image': item.image.url if item.image else None
                })
            except NoReverseMatch:
                continue

        # About page content search (all link to the main about page)
        about_configs = {
            'About': {'model': About, 'search_fields': ['title', 'content'], 'title_field': 'title', 'desc_field': 'content', 'img_field': None},
            'About Section': {'model': AboutContent, 'search_fields': ['section_title', 'section_content'], 'title_field': 'section_title', 'desc_field': 'section_content', 'img_field': 'image'},
            'Global Presence': {'model': GlobalPresence, 'search_fields': ['title', 'description_one'], 'title_field': 'title', 'desc_field': 'description_one', 'img_field': None},
            'Sustainability': {'model': Sustainability, 'search_fields': ['title', 'description'], 'title_field': 'title', 'desc_field': 'description', 'img_field': 'image'},
        }
        for type_name, config in about_configs.items():
            items = config['model'].objects.filter(build_search_q(query, config['search_fields'])).distinct()
            for item in items:
                try:
                    image_url = getattr(item, config['img_field'], None) and getattr(item, config['img_field']).url if config['img_field'] else None
                    results.append({
                        'title': getattr(item, config['title_field']),
                        'description': getattr(item, config['desc_field']),
                        'url': reverse('about:about'),
                        'type': type_name,
                        'image': image_url
                    })
                except (NoReverseMatch, AttributeError):
                    continue

        # Brands page content search (all link to the main brands page)
        brand_configs = {
            'Brand Guideline': {'model': BrandGuidelineDocument, 'search_fields': ['title', 'short_content'], 'title_field': 'title', 'desc_field': 'short_content', 'img_field': 'preview_image'},
            'Promo Materials': {'model': PromoMaterialsLibrary, 'search_fields': ['short_content', 'description'], 'title_field': 'short_content', 'desc_field': 'description', 'img_field': None},
            'Promo Material': {'model': PromoMaterial, 'search_fields': ['title'], 'title_field': 'title', 'desc_field': None, 'img_field': 'preview_image'},
            'Image Library': {'model': BrandImageLibrary, 'search_fields': ['short_content', 'description'], 'title_field': 'short_content', 'desc_field': 'description', 'img_field': None},
            'Video Library': {'model': BrandVideoLibrary, 'search_fields': ['short_content', 'description'], 'title_field': 'short_content', 'desc_field': 'description', 'img_field': None},
        }
        for type_name, config in brand_configs.items():
            items = config['model'].objects.filter(build_search_q(query, config['search_fields'])).distinct()
            for item in items:
                try:
                    desc_text = getattr(item, config['desc_field']) if config['desc_field'] else ''
                    if type_name == 'Promo Material':
                        desc_text = item.library.short_content if hasattr(item, 'library') else ''
                    
                    image_url = getattr(item, config['img_field'], None) and getattr(item, config['img_field']).url if config['img_field'] else None
                    results.append({
                        'title': getattr(item, config['title_field']),
                        'description': desc_text,
                        'url': reverse('brands:brands'),
                        'type': type_name,
                        'image': image_url
                    })
                except (NoReverseMatch, AttributeError):
                    continue
        
        # Services page content search
        service_configs = {
            'Service': {'model': Services, 'search_fields': ['title', 'description'], 'title_field': 'title', 'desc_field': 'description', 'img_field': 'image'},
            'Service Content': {'model': Service_Content, 'search_fields': ['subtitle', 'title', 'description'], 'title_field': 'title', 'desc_field': 'description', 'img_field': 'image'},
        }
        for type_name, config in service_configs.items():
            items = config['model'].objects.filter(build_search_q(query, config['search_fields'])).distinct()
            for item in items:
                try:
                    image_url = getattr(item, config['img_field'], None) and getattr(item, config['img_field']).url if config['img_field'] else None
                    results.append({
                        'title': getattr(item, config['title_field']),
                        'description': getattr(item, config['desc_field']),
                        'url': reverse('services:services'),
                        'type': type_name,
                        'image': image_url
                    })
                except (NoReverseMatch, AttributeError):
                    continue

        # Partnership page content search
        partnership_items = Partnership_Content.objects.filter(build_search_q(query, ['subtitle', 'title', 'description'])).distinct()
        for item in partnership_items:
            try:
                results.append({
                    'title': item.title,
                    'description': item.description,
                    'url': reverse('partnership:partnership'),
                    'type': 'Partnership',
                    'image': item.image.url if item.image else None
                })
            except NoReverseMatch:
                continue

        # FAQ search
        faqs = FAQ.objects.filter(build_search_q(query, ['question', 'answer']), is_active=True).distinct()
        for item in faqs:
            try:
                results.append({
                    'title': item.question,
                    'description': item.answer,
                    'url': reverse('faq:faq'),
                    'type': 'FAQ',
                    'image': None
                })
            except NoReverseMatch:
                continue
        
        # Reviews search
        reviews = Review.objects.filter(build_search_q(query, ['first_name', 'surname', 'summary', 'review']), is_approved=True).distinct()
        for item in reviews:
            try:
                results.append({
                    'title': f'Review by {item.full_name} - {item.rating}★',
                    'description': item.summary or item.review,
                    'url': reverse('home:home') + '#reviews',
                    'type': 'Review',
                    'image': None
                })
            except NoReverseMatch:
                continue

        # Remove duplicates based on URL and Title
        seen = set()
        unique_results = []
        for result in results:
            if result.get('description'):
                description_text = str(result['description'])
                result['description'] = description_text[:200] + '...' if len(description_text) > 200 else description_text
            
            identifier = (result['url'], result['title'])
            if identifier not in seen:
                unique_results.append(result)
                seen.add(identifier)
        
        results = unique_results
        total_results = len(results)

        # Relevance scoring and sorting
        def calculate_relevance(result):
            score = 0
            title_lower = str(result['title']).lower()
            desc_lower = str(result.get('description', '')).lower()
            query_lower = query.lower()
            
            if query_lower in title_lower:
                score += 100
            
            words = query_lower.split()
            for word in words:
                if len(word) > 1:
                    if word in title_lower:
                        score += 20
                    if word in desc_lower:
                        score += 10
            return score

        results.sort(key=calculate_relevance, reverse=True)

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