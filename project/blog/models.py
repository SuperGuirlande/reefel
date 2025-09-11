from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=255, unique=True)
    slug = models.SlugField(verbose_name="Slug", max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Générer un slug unique
        test = slugify(self.name)
        nb = 1
        unique = test

        while Category.objects.filter(slug=unique).exists():
            unique = f"{test}-{nb}"
            nb += 1

        self.slug = unique

        # Enregistrer la catégorie
        super().save(*args, **kwargs)



class Post(models.Model):
    title = models.CharField(verbose_name="Titre", max_length=255)
    slug = models.SlugField(verbose_name="Slug", max_length=100, blank=True, unique=True)

    introduction = models.TextField(verbose_name="Introduction")
    thumbnail = models.ImageField(verbose_name="Image de couverture", upload_to="blog/images/", null=True, blank=True)
    thumbnail_caption = models.CharField(verbose_name="Légende de l'image", max_length=255, null=True, blank=True)

    content = CKEditor5Field(verbose_name="Contenu", config_name='blog')
    categories = models.ManyToManyField(Category, verbose_name="Catégories")

    author = models.ForeignKey(CustomUser, verbose_name="Auteur", on_delete=models.SET_NULL, null=True, blank=True)


    created_at = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date de mise à jour", auto_now=True)

    def __str__(self):
        return f"Article: {self.title}"

    def save(self, *args, **kwargs):
        # Générer un slug unique
        test = slugify(self.title)
        nb = 1
        unique = test

        while Category.objects.filter(slug=unique).exists():
            unique = f"{test}-{nb}"
            nb += 1

        self.slug = unique

        # Enregistrer la catégorie
        super().save(*args, **kwargs)
