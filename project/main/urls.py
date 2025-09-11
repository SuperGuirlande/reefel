from django.urls import path
from .views import index, contact
from django.conf import settings
from django.conf.urls.static import static 

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('contact', contact, name='contact'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
