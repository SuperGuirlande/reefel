from django.urls import path, include
from .views import change_contact_infos, change_user_names_form, change_user_email_form

app_name = 'contact_management'

urlpatterns = [
    path('modifier-infos-de-contact/', change_contact_infos, name='change_contact_infos'),
    path('modifier-infos-de-compte/', change_user_names_form, name='change_user_names_form'),
    path('modifier-email-de-connexion/', change_user_email_form, name='change_user_email_form'),
]