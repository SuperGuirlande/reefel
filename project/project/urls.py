from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

