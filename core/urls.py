from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /media/private/",
        "",
        "Sitemap: https://maximum.de/sitemap.xml"
    ]
    return HttpResponse('\n'.join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('', include('product.urls')),
    path('', include('services.urls')),
    path('', include('about.urls')),
    path('', include('partnership.urls')),
    path('', include('faq.urls')),
    path('', include('news.urls')),
    path('', include('brands.urls')),
    path('', include('contact.urls')),
    path('', include('search.urls')),
    prefix_default_language=False
    )

urlpatterns += [
    re_path(r'^rosetta/', include('rosetta.urls'))
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)

handler404 = 'home.views.handler404'
handler403 = 'home.views.handler403'
handler500 = 'home.views.handler500'
handler503 = 'home.views.handler503'