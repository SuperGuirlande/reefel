from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Post.objects.filter(published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('blog:article_detail', kwargs={'slug': obj.slug})


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Category.objects.all()
    
    def location(self, obj):
        return reverse('blog:blog_category', kwargs={'category_slug': obj.slug})


class BlogIndexSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return ['blog:index']
    
    def location(self, item):
        return reverse(item)
