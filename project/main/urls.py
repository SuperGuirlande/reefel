from django.urls import path
from .views import index, robots_txt, sitemap_xml
from django.conf import settings
from django.conf.urls.static import static 

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
