from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogSitemap, CategorySitemap, BlogIndexSitemap, MainSitemap
from contact_management.forms import ContactForm
from django.contrib import messages
import os
from django.conf import settings


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message à été envoyé avec succès')
            messages.success(request, 'Vous serez contactez d\'ici 48 heures')
            return HttpResponseRedirect(f"{reverse('main:index')}#contact")
        else:
            messages.error(request, 'Veuillez vérifier les informations du formulaire')
    else:
        form = ContactForm()


    user = request.user
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'main/index.html', context)


@cache_page(60 * 60 * 24)  # Cache 24h
def robots_txt(request):
    """Vue pour servir le fichier robots.txt"""
    robots_path = os.path.join(settings.STATICFILES_DIRS[0], 'robots.txt')
    
    try:
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer l'URL du sitemap par l'URL réelle
        content = content.replace(
            'https://www.reefel.fr/sitemap.xml',
            f'{request.scheme}://{request.get_host()}/sitemap.xml'
        )
        
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse('User-agent: *\nDisallow: /', content_type='text/plain')


# Configuration des sitemaps
sitemaps = {
    'main': MainSitemap,
    'blog_index': BlogIndexSitemap,
    'blog_articles': BlogSitemap,
    'blog_categories': CategorySitemap,
}

@cache_page(60 * 60 * 12)  # Cache 12h
def sitemap_xml(request):
    """Vue pour servir la sitemap avec le bon Content-Type"""
    return sitemap(request, sitemaps, template_name='sitemap.xml', content_type='application/xml')

