from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, PostForm
from .models import Category, Post
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone


# USER #

def blog_index(request, category_slug=None):
    # Récupérer seulement les articles publiés
    articles = Post.objects.filter(published=True).select_related('author').prefetch_related('categories')
    categories = Category.objects.all()
    
    # Filtrage par catégorie (priorité à l'URL slug)
    category_filter = category_slug or request.GET.get('category')
    current_category_obj = None
    
    if category_filter:
        try:
            current_category_obj = get_object_or_404(Category, slug=category_filter)
            articles = articles.filter(categories=current_category_obj)
        except Http404:
            # Si la catégorie n'existe pas, on redirige vers l'index
            return redirect('blog:index')
    
    # Recherche dans titre, contenu et mots-clés
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(introduction__icontains=search_query) |
            Q(keywords__icontains=search_query)
        ).distinct()
    
    # Tri par date
    sort_by = request.GET.get('sort', 'created_desc')
    if sort_by == 'created_desc':
        articles = articles.order_by('-created_at')
    elif sort_by == 'created_asc':
        articles = articles.order_by('created_at')
    elif sort_by == 'updated_desc':
        articles = articles.order_by('-updated_at')
    elif sort_by == 'updated_asc':
        articles = articles.order_by('updated_at')
    else:
        articles = articles.order_by('-created_at')

    # Pagination
    paginator = Paginator(articles, 9)  # 9 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Métadonnées SEO
    if current_category_obj:
        page_title = f"Articles {current_category_obj.name} - Reefel Workshop"
        page_description = f"Découvrez nos articles sur {current_category_obj.name} et l'entretien de bateaux à La Rochelle."
    else:
        page_title = "Blog - Actualités & Conseils Nautiques | Reefel Workshop"
        page_description = "Découvrez nos derniers articles sur l'entretien et la réparation de bateaux. Conseils d'experts nautiques à La Rochelle."

    context = {
        'articles': page_obj,
        'categories': categories,
        'current_category': category_filter,
        'current_category_obj': current_category_obj,
        'current_search': search_query or '',
        'current_sort': sort_by,
        'page_title': page_title,
        'page_description': page_description,
        'page_keywords': 'blog nautique, entretien bateau, réparation bateau, conseils nautiques, La Rochelle',
    }

    return render(request, 'blog/user/index.html', context)

def article_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    
    # Vérifier que l'article est publié
    if not post.published:
        raise Http404("Article non trouvé")
    
    author = post.author
    author_name = "Auteur inconnu"
    
    if author:
        if author.first_name and author.last_name:
            author_name = f"{author.first_name} {author.last_name}"
        else:
            author_name = author.username

    # Articles relatifs
    related_articles = []
    
    # 1. Chercher des articles avec les mêmes catégories
    if post.categories.exists():
        related_articles = Post.objects.filter(
            categories__in=post.categories.all(),
            published=True
        ).exclude(id=post.id).distinct().order_by('-created_at')[:6]
    
    # 2. Si pas assez d'articles relatifs, compléter avec les plus récents
    if len(related_articles) < 4:
        recent_articles = Post.objects.filter(
            published=True
        ).exclude(
            id=post.id
        ).exclude(
            id__in=[article.id for article in related_articles]
        ).order_by('-created_at')[:4 - len(related_articles)]
        
        related_articles = list(related_articles) + list(recent_articles)

    # Métadonnées SEO
    page_title = f"{post.title} | Reefel Workshop Blog"
    page_description = post.introduction[:160] if post.introduction else f"Découvrez {post.title} sur notre blog nautique."
    
    # Mots-clés combinés
    keywords_list = []
    if post.keywords:
        keywords_list.extend(post.keywords.split(','))
    for category in post.categories.all():
        keywords_list.append(category.name)
    keywords_list.extend(['blog nautique', 'entretien bateau', 'La Rochelle'])
    page_keywords = ', '.join(set(keywords_list))

    context = {
        'post': post,
        'author_name': author_name,
        'related_articles': related_articles,
        'page_title': page_title,
        'page_description': page_description,
        'page_keywords': page_keywords,
    }

    return render(request, 'blog/user/article_detail.html', context)




# ADMIN #

### GESTION DU BLOG ###

# Index blog admin
def admin_blog_index(request):
    categories = Category.objects.all()
    posts = Post.objects.all()

    context = {
        'categories': categories,
        'posts': posts
    }
    return render(request, 'blog/admin/index.html', context)

# CRÉER ET MODIFIER LES CATEGORIES

# Page de formulaire de création de catégorie
def admin_category_form(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            name = category.name
            messages.success(request, f'La catégorie "{name}" a été créée avec succès.')
            return redirect('blog:admin_index')
    else:
        form = CategoryForm()
    return render(request, 'blog/admin/category_form.html', {'form': form})


# Fonction de création de catégorie en AJAX
def create_category_ajax(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            name = data.get('name') or data.get('category_name')  # Support des deux formats

            if not name:
                return JsonResponse({'success': False, 'error': 'Le nom de la catégorie est requis'})
            
            if Category.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'La catégorie existe déjà'})

            category = Category.objects.create(name=name)
            return JsonResponse({
                'success': True, 
                'category': {
                    'id': category.id, 
                    'name': category.name,
                    'slug': category.slug
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Données JSON invalides'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



# Créer et modifier les articles
def admin_post_form(request, post_slug=None):
    post = None
    if post_slug:
        post = Post.objects.get(slug=post_slug)

    if request.method == 'POST':
        if post:
            form = PostForm(request.POST, request.FILES, instance=post)
        else:
            form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.author:
                post.author = request.user
            post.save()
            return redirect('blog:admin_index')
    else:
        if post:
            form = PostForm(instance=post)
        else:
            form = PostForm()

    return render(request, 'blog/admin/post_form.html', {'form': form})

# Supprimer les articles
def confirm_delete_article(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    return render(request, 'blog/admin/confirm_delete_article.html', {'post': post})

def admin_post_delete(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    post.delete()
    messages.success(request, f'L\'article "{post.title}" a été supprimé avec succès.')
    return redirect('blog:admin_index')

# Supprimer les catégories
def confirm_delete_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    return render(request, 'blog/admin/confirm_delete_category.html', {'category': category})

def admin_category_delete(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    category.delete()
    messages.success(request, f'La catégorie "{category.name}" a été supprimée avec succès.')
    return redirect('blog:admin_index')