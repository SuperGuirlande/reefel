from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings


def test_email(request):
    """
    Vue de test pour vérifier l'envoi d'emails
    """
    if not settings.DEBUG:
        return HttpResponse("Cette vue n'est disponible qu'en mode DEBUG")
    
    try:
        # Test d'envoi d'email
        result = send_mail(
            subject='🧪 Test Email REEFEL',
            message='Ceci est un email de test pour vérifier la configuration SMTP.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['votre-email@example.com'],  # Remplacez par votre email
            fail_silently=False,
        )
        
        if result:
            return HttpResponse("✅ Email envoyé avec succès !")
        else:
            return HttpResponse("❌ Échec de l'envoi de l'email")
            
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors de l'envoi: {str(e)}")