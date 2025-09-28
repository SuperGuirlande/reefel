from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_page
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
            'https://votre-domaine.com/sitemap.xml',
            f'{request.scheme}://{request.get_host()}/sitemap.xml'
        )
        
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse('User-agent: *\nDisallow: /', content_type='text/plain')

