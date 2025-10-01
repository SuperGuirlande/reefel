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
    # Construction de l'URL du sitemap dynamiquement
    sitemap_url = f'{request.scheme}://{request.get_host()}/sitemap.xml'
    
    # Contenu du robots.txt optimisé
    robots_content = f"""User-agent: *
Allow: /

# Pages importantes à indexer
Allow: /blog/
Allow: /blog/article/
Allow: /blog/categorie/

# Pages à exclure de l'indexation
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
Sitemap: {sitemap_url}

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
    from django.contrib.sites.models import Site
    from django.conf import settings
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    
    # Construire l'URL de base correcte
    if settings.DEBUG:
        base_url = f"{request.scheme}://{request.get_host()}"
    else:
        site = Site.objects.get_current()
        base_url = f"https://{site.domain}"
    
    # Générer le contenu XML manuellement pour contrôler les URLs
    urls = []
    
    # Page d'accueil
    urls.append({
        'loc': f"{base_url}/",
        'lastmod': '2025-10-01',
        'changefreq': 'weekly',
        'priority': '1.0'
    })
    
    # Blog index
    urls.append({
        'loc': f"{base_url}/blog/",
        'lastmod': '2025-09-28',
        'changefreq': 'daily',
        'priority': '0.9'
    })
    
    # Articles de blog
    from blog.models import Post
    for post in Post.objects.filter(published=True):
        urls.append({
            'loc': f"{base_url}/blog/article/{post.slug}/",
            'lastmod': post.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.9'
        })
    
    # Catégories
    from blog.models import Category
    for category in Category.objects.all():
        urls.append({
            'loc': f"{base_url}/blog/categorie/{category.slug}/",
            'changefreq': 'monthly',
            'priority': '0.6'
        })
    
    context = {'urls': urls}
    xml_content = render_to_string('main/sitemap.xml', context)
    
    return HttpResponse(xml_content, content_type='application/xml')

