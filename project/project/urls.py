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
    # Essayer d'abord dans main/static, puis dans staticfiles
    robots_paths = [
        os.path.join(settings.STATICFILES_DIRS[0], 'robots.txt'),
        os.path.join(settings.STATIC_ROOT, 'robots.txt')
    ]
    
    for robots_path in robots_paths:
        try:
            with open(robots_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HttpResponse(content, content_type='text/plain')
        except FileNotFoundError:
            continue
    
    # Fallback si le fichier n'existe pas
    return HttpResponse("User-agent: *\nAllow: /", content_type='text/plain')

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

