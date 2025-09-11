from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=100, verbose_name="Slug de la catégorie", unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Génération d'un slug unique
        if not self.slug:
            test = slugify(self.name)
            unique = test
            nb = 1
            while Category.objects.filter(slug=unique).exists():
                unique = f"{test}-{nb}"
                nb += 1
            self.slug = unique
        # Sauvegarde
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Catégorie : {self.name}"


class SubCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de la sous-catégorie")
    slug = models.SlugField(max_length=100, verbose_name="Slug de la sous-catégorie", unique=True, blank=True)

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Catégorie associée")

    def save(self, *args, **kwargs):
        # Génération d'un slug unique
        if not self.slug:
            test = slugify(self.name)
            unique = test
            nb = 1
            while SubCategory.objects.filter(slug=unique).exists():
                unique = f"{test}-{nb}"
                nb += 1
            self.slug = unique
        # Sauvegarde
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom du produit", unique=True)
    slug = models.SlugField(max_length=100, verbose_name="Slug du produit", unique=True, blank=True)
    categories = models.ManyToManyField(to=SubCategory, related_name="products")

    thumbnail = models.ImageField(verbose_name="Miniature de l'article", upload_to="shop/miniatures")

    price = models.DecimalField(max_digits=5, decimal_places=2)
    reduction = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], default=0)
    final_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    description = CKEditor5Field(config_name='blog', blank=True, null=True)


    def save(self, *args, **kwargs):
        # Prix par defaut
        if not self.final_price:
            self.final_price = self.price

        # Appliquer la réduction
        if self.reduction != 0:
            reduction = self.price * (self.reduction / 100)
            self.final_price = self.price - reduction
        else:
            self.final_price = self.price

        # Génération d'un slug unique
        if not self.slug:
            test = slugify(self.name)
            unique = test
            nb = 1
            while Product.objects.filter(slug=unique).exists():
                unique = f"{test}-{nb}"
                nb += 1
            self.slug = unique
        # Sauvegarde
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    file = models.ImageField(verbose_name="Fichier image", upload_to="shop/images")
    caption = models.CharField(verbose_name="Caption de l'image", max_length=255)
    slug = models.SlugField(max_length=100, verbose_name="Slug de l'image", unique=True, blank=True)

    product = models.ForeignKey(Product, models.CASCADE, related_name='images', verbose_name="Produit associé")

    def save(self, *args, **kwargs):
        # Génération d'un slug unique
        if not self.slug:
            test = slugify(self.caption)
            unique = test
            nb = 1
            while ProductImage.objects.filter(slug=unique).exists():
                unique = f"{test}-{nb}"
                nb += 1
            self.slug = unique
        # Sauvegarde
        super().save(*args, **kwargs)
