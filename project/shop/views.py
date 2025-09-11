from django.shortcuts import render
from .models import Category, SubCategory, Product
from accounts.models import CustomUser
from django.http import HttpResponse, JsonResponse


def admin_shop_index(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    products = Product.objects.all()

    customers = CustomUser.objects.exclude(is_superuser=True)


    context = {
        'categories': categories,
        'subcategories': subcategories,
        'products': products,
        'customers': customers
        
    }
    return render(request, 'shop/admin/index.html', context)


def admin_shop_categories(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    context = {
        'categories': categories,
        'subcategories': subcategories,
        
    }
    return render(request, 'shop/admin/categories.html', context)


# Fonction de création de catégorie en AJAX
def create_category_ajax(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            name = data.get('category_name')
            category_type = data.get('category_type')
            parent_category_id = data.get('parent_category_id')

            if not name or not category_type:
                return JsonResponse({'success': False, 'error': 'Le nom de la catégorie est requis'})
            
            if category_type == 'category':
                if Category.objects.filter(name=name).exists():
                    return JsonResponse({'success': False, 'error': 'La catégorie existe déjà'})

                category = Category.objects.create(name=name)
                return JsonResponse({'success': True, 'category': {'id': category.id, 'name': category.name}})
                
            elif category_type == 'subcategory':
                if not parent_category_id:
                    return JsonResponse({'success': False, 'error': 'Une catégorie parent est requise'})
                
                try:
                    parent_category = Category.objects.get(id=parent_category_id)
                except Category.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'La catégorie parent n\'existe pas'})
                
                if SubCategory.objects.filter(name=name, category=parent_category).exists():
                    return JsonResponse({'success': False, 'error': 'Cette sous-catégorie existe déjà pour cette catégorie'})

                subcategory = SubCategory.objects.create(name=name, category=parent_category)
                return JsonResponse({
                    'success': True, 
                    'subcategory': {
                        'id': subcategory.id, 
                        'name': subcategory.name,
                        'parent_id': parent_category.id,
                        'parent_name': parent_category.name
                    }
                })
            

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Données JSON invalides'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Fonction de suppression de catégorie en AJAX
def delete_category_ajax(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            category_id = data.get('category_id')
            category_type = data.get('category_type')

            if not category_id or not category_type:
                return JsonResponse({'success': False, 'error': 'Données manquantes'})
            
            if category_type == 'category':
                try:
                    category = Category.objects.get(id=category_id)
                    category_name = category.name
                    category.delete()  # Supprime aussi les sous-catégories via CASCADE
                    return JsonResponse({'success': True, 'message': f'Catégorie "{category_name}" supprimée'})
                except Category.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'La catégorie n\'existe pas'})
                    
            elif category_type == 'subcategory':
                try:
                    subcategory = SubCategory.objects.get(id=category_id)
                    subcategory_name = subcategory.name
                    subcategory.delete()
                    return JsonResponse({'success': True, 'message': f'Sous-catégorie "{subcategory_name}" supprimée'})
                except SubCategory.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'La sous-catégorie n\'existe pas'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Données JSON invalides'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})