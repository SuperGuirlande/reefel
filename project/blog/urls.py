from django.urls import path, include
from .views import (
    admin_blog_index,
    admin_category_form,
    admin_post_form,
    confirm_delete_category,
    admin_category_delete,
    admin_post_delete,
    create_category_ajax,
    article_detail,
    confirm_delete_article,
    blog_index
)

app_name = 'blog'

urlpatterns = [
    # USER #
    path('', blog_index, name="index"),
    path('categorie/<slug:category_slug>/', blog_index, name='blog_category'),
    path('article/<slug:slug>/', article_detail, name='article_detail'),

    # ADMIN #
    path('admin/', admin_blog_index, name='admin_index'),
    path('admin/creer-une-categorie/', admin_category_form, name='admin_category_form'),
    path('admin/creer-un-article/', admin_post_form, name='admin_post_form'),
    path('admin/modifier-un-article/<str:post_slug>/', admin_post_form, name='admin_change_post_form'),

    path('admin/confirmer-la-suppression-categorie/<slug:category_slug>/', confirm_delete_category, name='confirm_delete_category'),
    path('admin/supprimer-une-categorie/<slug:category_slug>/', admin_category_delete, name='admin_category_delete'),

    path('admin/confirmer-la-suppression-article/<slug:post_slug>/', confirm_delete_article, name='confirm_delete_article'),
    path('admin/supprimer-un-article/<slug:post_slug>/', admin_post_delete, name='admin_post_delete'),

    path('ajax/create-category/', create_category_ajax, name='create_category_ajax'),
]