import re
from django.db import models
from django.utils import timezone

# Create your models here.
def format_phone_number(phone_number: str) -> str:
    """Normalise et formate un numéro FR en « 06 12 34 56 78 ».
    """
    digits = re.sub(r"\D", "", phone_number)
    if digits.startswith("33") and len(digits) == 11:  # ex: 33612345678
        digits = "0" + digits[2:]
    if len(digits) != 10:
        raise ValueError("Un numéro français doit contenir 10 chiffres.")
    return " ".join(digits[i : i + 2] for i in range(0, 10, 2))


class ContactInfos(models.Model):
    phone = models.CharField(max_length=16, verbose_name="Téléphone")
    email = models.EmailField(max_length=254, verbose_name="Email")

    class Meta:
        verbose_name = "Informations de contact"
        verbose_name_plural = "Informations de contact"
                    
    def __str__(self):
        return f"Contact du site : {self.phone} - {self.email}"
    
    def save(self, *args, **kwargs):
        # Formatage du numéro de téléphone
        self.phone = format_phone_number(self.phone)
        super().save(*args, **kwargs)



class ContactMessage(models.Model):
    class Subjects(models.TextChoices):
        DEVIS = 'devis', 'Demande de devis'
        RDV = 'rdv', 'Demande de rendez-vous'
        INFO = 'info', 'Demande d\'information'
        AUTRE = 'autre', 'Autre demande'

    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    last_name = models.CharField(max_length=255, verbose_name="Nom")

    phone = models.CharField(verbose_name="N° de téléphone", max_length=16)
    email = models.EmailField()

    subject = models.CharField(max_length=255, choices=Subjects.choices, verbose_name="Sujet de votre message", blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de reception")

    cgv_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.first_name} {self.last_name} - {self.created_at.strftime('%d/%m/%Y à %H:%M')}"