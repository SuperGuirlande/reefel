from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.decorators.http import require_GET
import os

@require_GET
def robots_txt(request):
    """Vue pour servir le fichier robots.txt"""
    # Contenu direct du robots.txt (pas de dépendance aux chemins)
    robots_content = """User-agent: *
Allow: /

# Pages importantes
Allow: /blog/
Allow: /blog/article/
Allow: /blog/categorie/

# Pages à exclure
Disallow: /admin/
Disallow: /compte/
Disallow: /contact/
Disallow: /ckeditor5/
Disallow: /static/admin/
Disallow: /media/blog/images/

# Fichiers à exclure
Disallow: *.pdf$
Disallow: *.doc$
Disallow: *.docx$
Disallow: *.xls$
Disallow: *.xlsx$

# Sitemap
Sitemap: https://www.reefel.fr/sitemap.xml

# Crawl-delay pour éviter la surcharge
Crawl-delay: 1

# User-agent spécifique pour Google
User-agent: Googlebot
Allow: /
Crawl-delay: 0

# User-agent spécifique pour Bing
User-agent: Bingbot
Allow: /
Crawl-delay: 1

# User-agent spécifique pour Facebook
User-agent: facebookexternalhit
Allow: /
Crawl-delay: 0"""
    
    return HttpResponse(robots_content, content_type='text/plain')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # Global
    path('compte/', include('accounts.urls')),
    path('', include('main.urls')),

    # Apps
    path('blog/', include('blog.urls')),
    path('contact/', include('contact_management.urls')),
    
    # Robots.txt
    path('robots.txt', robots_txt, name='robots_txt'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

