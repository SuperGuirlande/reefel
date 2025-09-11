from django import forms
from django.contrib.auth import get_user_model
from project import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Adresse e-mail"), 
        widget=forms.TextInput(
            attrs={
                'class': 'form-field form-charfield',
                'placeholder': 'exemple@email.com'
                }
            )
        )
    password = forms.CharField(
        label=_('Password'), 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field form-charfield',
                'placeholder': '********'
                }
            )
        )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_('Ancien mot de passe'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field form-charfield',
                'placeholder': '********'
            }
        )
    )
    new_password = forms.CharField(
        label=_('Nouveau mot de passe'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field form-charfield',
                'placeholder': '********'
            }
        )
    )
    confirm_password = forms.CharField(
        label=_('Confirmer le nouveau mot de passe'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-field form-charfield',
                'placeholder': '********'
            }
        )
    )
