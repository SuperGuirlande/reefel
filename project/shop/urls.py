from django.urls import path
from .views import (
    admin_shop_index,
    admin_shop_categories,
    create_category_ajax,
    delete_category_ajax
)

app_name = 'shop'

urlpatterns = [
    path('admin', admin_shop_index, name="admin_index"),
    path('admin/categories', admin_shop_categories, name="admin_categories"),
    path('admin/categories/creer-categorie-ajax', create_category_ajax, name="create_category_ajax"),
    path('admin/categories/supprimer-categorie-ajax', delete_category_ajax, name="delete_category_ajax")
]