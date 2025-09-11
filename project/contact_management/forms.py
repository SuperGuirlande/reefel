from django import forms
from django.utils.safestring import mark_safe
from .models import ContactInfos, format_phone_number, ContactMessage
from accounts.models import CustomUser


class ContactForm(forms.ModelForm):
    subject = forms.ChoiceField(
        choices=[('', 'Quel est le sujet de votre message')] + list(ContactMessage.Subjects.choices),
        required=True,
        widget=forms.Select(attrs={'class': 'form-field form-charfield'})
    )
    cgv_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-field form-checkbox'})
    )
    
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'phone', 'email', 'subject', 'message', 'cgv_accepted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'John'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Doe'
        self.fields['phone'].widget.attrs['placeholder'] = '06 12 34 56 78'
        self.fields['email'].widget.attrs['placeholder'] = 'contact@example.com'
        self.fields['message'].widget.attrs['placeholder'] = 'Laissez nous votre message'

        self.fields['first_name'].widget.attrs['class'] = 'form-field form-charfield'
        self.fields['last_name'].widget.attrs['class'] = 'form-field form-charfield'
        self.fields['phone'].widget.attrs['class'] = 'form-field form-charfield'
        self.fields['email'].widget.attrs['class'] = 'form-field form-charfield'
        self.fields['message'].widget.attrs['class'] = 'form-field form-charfield'
        self.fields['cgv_accepted'].widget.attrs['class'] = 'form-field form-checkbox'

    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            # Tester le formatage sans sauvegarder
            format_phone_number(phone)
            return phone
        except ValueError as e:
            raise forms.ValidationError(mark_safe("Format de téléphone invalide. <br>Veuillez saisir un numéro français valide (ex: 06 12 34 56 78)"))


class ContactInfosForm(forms.ModelForm):
    class Meta:
        model = ContactInfos
        fields = ['phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['placeholder'] = '06 12 34 56 78'
        self.fields['email'].widget.attrs['placeholder'] = 'contact@example.com'
        self.fields['phone'].widget.attrs['class'] = 'form-field form-charfield'
        self.fields['email'].widget.attrs['class'] = 'form-field form-charfield'
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            # Tester le formatage sans sauvegarder
            format_phone_number(phone)
            return phone
        except ValueError as e:
            raise forms.ValidationError(mark_safe("Format de téléphone invalide. <br>Veuillez saisir un numéro français valide (ex: 06 12 34 56 78)"))
            

class ChangeUserNamesForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Prénom",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-field form-charfield'}),
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-field form-charfield'}),
    )
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-field form-charfield'}),
    )
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']


class ChangeUserEmailForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-field form-charfield'}),
    )
    class Meta:
        model = CustomUser
        fields = ['email']