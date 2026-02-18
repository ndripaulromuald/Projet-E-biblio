from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Livre(models.Model):

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
        return dict(self.CATEGORIES).get(self.categorie, self.categorie)

    def note_moyenne(self):
        avis_list = self.avis.all()
        if avis_list.exists():
            total = sum([a.note for a in avis_list])
            return round(total / avis_list.count(), 1)
        return 0

    def nombre_avis(self):
        return self.avis.count()

    def get_etoiles_moyenne(self):
        moyenne = self.note_moyenne()
        etoiles_pleines = int(moyenne)
        demi_etoile = 1 if (moyenne - etoiles_pleines) >= 0.5 else 0
        etoiles_vides = 5 - etoiles_pleines - demi_etoile

        html = '★' * etoiles_pleines
        if demi_etoile:
            html += '⯨'
        html += '☆' * etoiles_vides
        return html


class Favori(models.Model):

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


class Avis(models.Model):

    NOTES = [
        (1, 'Très décevant'),
        (2, 'Décevant'),
        (3, 'Pas mal'),
        (4, 'Très bien'),
        (5, 'Excellent'),
    ]

    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name='avis',
        verbose_name="Livre"
    )
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur"
    )
    note = models.IntegerField(
        choices=NOTES,
        verbose_name="Note"
    )
    commentaire = models.TextField(
        verbose_name="Commentaire",
        help_text="Partagez votre avis sur ce livre"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    likes = models.ManyToManyField(
        User,
        related_name='avis_likes',
        blank=True,
        verbose_name="Likes"
    )

    class Meta:
        unique_together = ['livre', 'utilisateur']
        ordering = ['-date_creation']
        verbose_name = "Avis"
        verbose_name_plural = "Avis"

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre} ({self.note}/5)"

    def nombre_likes(self):
        return self.likes.count()

    def get_etoiles(self):
        etoiles_pleines = '★' * self.note
        etoiles_vides = '☆' * (5 - self.note)
        return etoiles_pleines + etoiles_vides