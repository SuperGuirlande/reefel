from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()

@register.filter
def truncate_words_html(value, limit):
    """
    Tronque le texte HTML en gardant les balises intactes
    """
    if not value:
        return ""
    
    # Compter les mots dans le texte sans les balises HTML
    text_only = re.sub(r'<[^>]+>', '', str(value))
    words = text_only.split()
    
    if len(words) <= limit:
        return value
    
    # Tronquer et ajouter "..."
    truncated_words = words[:limit]
    truncated_text = ' '.join(truncated_words)
    
    # Trouver la position de troncature dans le HTML original
    current_pos = 0
    word_count = 0
    
    for word in words:
        if word_count >= limit:
            break
        word_pos = text_only.find(word, current_pos)
        if word_pos != -1:
            current_pos = word_pos + len(word)
        word_count += 1
    
    # Tronquer le HTML à cette position
    html_truncated = str(value)[:current_pos] + "..."
    
    return mark_safe(html_truncated)


@register.filter
def clean_html(value):
    """
    Nettoie le HTML pour les meta descriptions
    """
    if not value:
        return ""
    
    # Supprimer les balises HTML
    clean = re.sub(r'<[^>]+>', '', str(value))
    # Supprimer les espaces multiples
    clean = re.sub(r'\s+', ' ', clean)
    # Supprimer les espaces en début/fin
    clean = clean.strip()
    
    return clean


@register.filter
def word_count(value):
    """
    Compte le nombre de mots dans un texte HTML
    """
    if not value:
        return 0
    
    # Supprimer les balises HTML et compter les mots
    text_only = re.sub(r'<[^>]+>', '', str(value))
    words = text_only.split()
    
    return len(words)


@register.simple_tag
def generate_meta_description(post, max_length=160):
    """
    Génère une meta description optimisée pour un article
    """
    if not post:
        return "Reefel Workshop - Spécialiste réparation et entretien de bateaux à La Rochelle"
    
    # Utiliser l'introduction si disponible
    if post.introduction:
        description = clean_html(post.introduction)
    else:
        # Extraire le début du contenu
        content = clean_html(post.content)
        description = content[:max_length]
    
    # Tronquer si nécessaire
    if len(description) > max_length:
        description = description[:max_length-3] + "..."
    
    # Ajouter des mots-clés pertinents
    keywords = []
    if post.categories.exists():
        keywords.extend([cat.name for cat in post.categories.all()[:2]])
    
    if keywords:
        description += f" - {', '.join(keywords)}"
    
    return escape(description)


@register.simple_tag
def generate_meta_keywords(post):
    """
    Génère des mots-clés optimisés pour un article
    """
    if not post:
        return "réparation bateau, entretien bateau, La Rochelle, Reefel Workshop"
    
    keywords = []
    
    # Mots-clés de l'article
    if post.keywords:
        keywords.extend([kw.strip() for kw in post.keywords.split(',')])
    
    # Catégories
    if post.categories.exists():
        keywords.extend([cat.name for cat in post.categories.all()])
    
    # Mots-clés génériques
    keywords.extend([
        "réparation bateau",
        "entretien bateau", 
        "La Rochelle",
        "Port des Minimes",
        "Reefel Workshop",
        "nautique"
    ])
    
    # Supprimer les doublons et limiter
    unique_keywords = list(dict.fromkeys(keywords))[:15]
    
    return escape(', '.join(unique_keywords))
