from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Livre(models.Model):
    """Modèle représentant un livre dans la bibliothèque"""

    CATEGORIES = [
        ('roman', 'Roman'),
        ('science', 'Science'),
        ('histoire', 'Histoire'),
        ('education', 'Éducation'),
        ('technologie', 'Technologie'),
        ('culture', 'Culture Africaine'),
        ('religion', 'Religion'),
        ('autre', 'Autre'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre")
    auteur = models.CharField(max_length=100, verbose_name="Auteur")
    description = models.TextField(verbose_name="Description")
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        verbose_name="Catégorie"
    )
    fichier_pdf = models.FileField(
        upload_to='livres/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Fichier PDF"
    )
    couverture = models.ImageField(
        upload_to='couvertures/',
        blank=True,
        null=True,
        verbose_name="Couverture"
    )
    ajoute_par = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Ajouté par"
    )
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    nombre_telechargements = models.IntegerField(default=0, verbose_name="Téléchargements")
    nombre_lectures = models.IntegerField(default=0, verbose_name="Lectures")

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Livre"
        verbose_name_plural = "Livres"

    def __str__(self):
        return self.titre

    def get_categorie_display_custom(self):
        """Retourne le nom complet de la catégorie"""
        return dict(self.CATEGORIES).get(self.categorie, self.categorie)


class Favori(models.Model):
    """Modèle représentant les favoris d'un utilisateur"""

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur"
    )
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        verbose_name="Livre"
    )
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        unique_together = ['utilisateur', 'livre']
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre}"