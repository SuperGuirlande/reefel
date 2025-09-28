from django.urls import path
from .views import index, robots_txt
from django.conf import settings
from django.conf.urls.static import static 

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
