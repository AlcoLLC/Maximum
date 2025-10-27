from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from product.models import Product
from news.models import News

class HomeSitemap(Sitemap):
    changefreq = 'daily' 
    priority = 1.0

    def items(self):
        return ['home:home']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse('product:product_detail', kwargs={'slug': obj.slug})


class NewsSitemap(Sitemap):
    changefreq = 'daily' 
    priority = 0.8

    def items(self):
        return News.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('news:news_detail', kwargs={'slug': obj.slug})

class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return [
            'about:about',
            'brands:brands',
            'contact:contact',
            'faq:faq',
            'news:news', 
            'partnership:partnership',
            'product:products',
            'services:services',
        ]

    def location(self, item):
        return reverse(item)


class ContactFormSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.4
    
    def items(self):
        return ['contact:contact_step_two']
        
    def location(self, item):
        return reverse(item)


sitemaps = {
    'home': HomeSitemap,
    'static-pages': StaticViewSitemap,
    'products': ProductSitemap,
    'news': NewsSitemap,
    'contact-form': ContactFormSitemap,
}
