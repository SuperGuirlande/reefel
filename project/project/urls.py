from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogSitemap, CategorySitemap, BlogIndexSitemap, MainSitemap

# Configuration des sitemaps
sitemaps = {
    'main': MainSitemap,
    'blog_index': BlogIndexSitemap,
    'blog_articles': BlogSitemap,
    'blog_categories': CategorySitemap,
}

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
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

