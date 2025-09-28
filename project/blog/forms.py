from django import forms
from .models import Post, Category
from django_ckeditor_5.widgets import CKEditor5Widget


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom", 
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-field form-charfield",
                "placeholder": "Nom de la catégorie"
            }
        )
    )
    slug = forms.SlugField(
        label="Slug",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-field form-charfield",
                "placeholder": "Slug de la catégorie"
            }
        )
    )

    class Meta:
        model = Category
        fields = ["name", "slug"]



class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Titre", 
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-field form-charfield",
                "placeholder": "Titre de l'article"
            }
        )
    )
    slug = forms.SlugField(
        label="Slug",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-field form-charfield",
                "placeholder": "Slug de l'article ( Facultatif )"
            }
        )
    )
    introduction = forms.CharField(
        label="Introduction",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-field form-textarea",
                "placeholder": "Introduction de l'article",
                "rows": 8
            }
        )
    )
    thumbnail = forms.ImageField(
        label="Miniature de l'article",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-field form-file",
                "placeholder": "Image de miniature de l'article"
            }
        )
    )
    thumbnail_caption = forms.CharField(
        label="Légende de l'image",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-field form-charfield",
                "placeholder": "Légende de la miniature (invisible, pour le référencement)"
            }
        )
    )
    content = forms.CharField(
        label="Contenu",
        required=True,
        widget=CKEditor5Widget(
            config_name="blog"
        )
    )
    categories = forms.ModelMultipleChoiceField(
        label="Catégories",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-checkbox"
            }
        )
    )

    published = forms.BooleanField(
        label="Publier sur le site",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": 'form-field form-checkbox'
            }
        )
    )

    class Meta:
        model = Post
        fields = ["title", "slug", "introduction", "thumbnail", "thumbnail_caption", "content", "categories", "published"]







