from django import forms
from .models import Product, Category, SubCategory


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


class SubCategoryForm(forms.ModelForm):
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
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        to_field_name='name',
        required=True,
        widget=forms.Select(
            attrs={
                'class': "form-field form-charfield"
            }
        )
    )

    class Meta:
        model = Category
        fields = ["name", "slug"]