from .models import ContactInfos
from django.utils import timezone

def create_default_contact_infos():
    contact_infos = ContactInfos.objects.create(
        phone="06 12 34 56 78",
        email="contact@test.fr",
    )
    contact_infos.save()

def contact_infos_context(request):
    contact_infos = ContactInfos.objects.first()

    if not contact_infos:
        contact_infos = create_default_contact_infos()

    return {
        'contact_infos': contact_infos,
        'current_year': timezone.now().year,
    }