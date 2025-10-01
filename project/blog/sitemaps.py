from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Post.objects.filter(published=True).select_related('author').prefetch_related('categories').order_by('-updated_at')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('blog:article_detail', kwargs={'slug': obj.slug})
    
    def priority(self, obj):
        # Articles récents ont une priorité plus élevée
        from django.utils import timezone
        from datetime import timedelta
        
        if obj.created_at > timezone.now() - timedelta(days=30):
            return 0.9
        elif obj.created_at > timezone.now() - timedelta(days=90):
            return 0.8
        else:
            return 0.7


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Category.objects.all().order_by('name')
    
    def location(self, obj):
        return reverse('blog:blog_category', kwargs={'category_slug': obj.slug})
    
    def lastmod(self, obj):
        # Dernière modification basée sur le dernier article de la catégorie
        last_post = Post.objects.filter(
            categories=obj, 
            published=True
        ).order_by('-updated_at').first()
        
        if last_post:
            return last_post.updated_at
        return None


class BlogIndexSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return ['blog:index']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        # Dernière modification basée sur le dernier article publié
        last_post = Post.objects.filter(published=True).order_by('-updated_at').first()
        if last_post:
            return last_post.updated_at
        return None


class MainSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0
    
    def items(self):
        return ['main:index']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        # Pour la page d'accueil, on peut utiliser la date de dernière modification du site
        from django.utils import timezone
        return timezone.now()
