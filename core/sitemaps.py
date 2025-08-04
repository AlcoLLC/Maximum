from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return [
            'home:home',
            'about:about',
            'products:product',
            'services: services', 
            'contact:contact',
            'partnership:partnership',
            'news:news',
            'faq:faq'
        ]
    
    def location(self, item):
        return reverse(item)




sitemaps = {
    'static': StaticViewSitemap,

}