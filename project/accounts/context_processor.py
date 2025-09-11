# Récupérer des urls
# URL sans paramètres GET 
# requete = request.path

# URL avec paramètres GET (/blog/article/123/?page=2&filter=news)
# current_full_path = request.get_full_path()

# URL complète avec domaine (https://monsite.com/blog/article/123/)
# current_absolute_url = request.build_absolute_uri()
 
# Trouver des urls préconstruites
# admin_url = reverse('accounts:admin_index')
# Résultat: /accounts/admin/

# URL avec paramètres
# article_url = reverse('blog:article_detail', kwargs={'slug': 'mon-article'})
# Résultat: /blog/article/mon-article/

# URL avec arguments positionnels
# user_url = reverse('accounts:user_profile', args=[user.id])
# Résultat: /accounts/user/123/


def get_active_links(request):
    global_link = None

    # URL sans paramètres GET 
    requete = request.path
    # URL avec paramètres GET (/blog/article/123/?page=2&filter=news)
    current_full_path = request.get_full_path()
    # URL complète avec domaine (https://monsite.com/blog/article/123/)
    current_absolute_url = request.build_absolute_uri()

    print(f"Requête simple : {requete}")

    ### ACTIVE LINKS GLOBAL ###
    # Home
    if requete == '/':
        global_link = 'home'
        print('Active Global : Home')
        
    # Blog
    if requete.startswith('/blog/'):
        global_link = 'blog'
        print('Active Global : Blog')

    return {
        'global_link': global_link,
    }