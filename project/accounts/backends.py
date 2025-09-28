import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


class CustomEmailBackend(EmailBackend):
    """
    Backend email personnalisé qui gère les problèmes de certificats SSL
    """
    
    def open(self):
        """
        Établit une connexion au serveur email avec une configuration SSL personnalisée
        """
        if self.connection:
            return False
        
        connection_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
        
        if self.use_ssl:
            # Créer un contexte SSL personnalisé qui ignore la vérification des certificats
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Établir la connexion avec le contexte SSL personnalisé
            try:
                self.connection = connection_class(
                    self.host, 
                    self.port,
                    context=context,
                    timeout=self.timeout
                )
                
                # Authentification
                if self.username and self.password:
                    self.connection.login(self.username, self.password)
                    
                return True
                
            except (smtplib.SMTPException, OSError) as e:
                if not self.fail_silently:
                    raise e
                return False
        else:
            # Pour les connexions non-SSL, utiliser le comportement par défaut
            return super().open()
    
    def _send(self, email_message):
        """
        Envoie un email avec gestion d'erreurs améliorée
        """
        if not email_message.recipients():
            return False
        
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = email_message.from_email
        recipients = email_message.recipients()
        message = email_message.message()
        
        try:
            self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))
        except (smtplib.SMTPException, OSError) as e:
            if not self.fail_silently:
                # Log l'erreur pour debug
                print(f"Erreur envoi email: {e}")
                raise e
            return False
        
        return True