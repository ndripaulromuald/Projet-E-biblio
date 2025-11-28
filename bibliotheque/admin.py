from django.contrib import admin
from .models import Livre, Favori

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'ajoute_par', 'date_ajout',
                    'nombre_telechargements', 'nombre_lectures']
    list_filter = ['categorie', 'date_ajout']
    search_fields = ['titre', 'auteur', 'description']
    readonly_fields = ['date_ajout', 'nombre_telechargements', 'nombre_lectures']

    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'auteur', 'description', 'categorie')
        }),
        ('Fichiers', {
            'fields': ('fichier_pdf', 'couverture')
        }),
        ('Métadonnées', {
            'fields': ('ajoute_par', 'date_ajout', 'nombre_telechargements', 'nombre_lectures')
        }),
    )

@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'livre', 'date_ajout']
    list_filter = ['date_ajout']
    search_fields = ['utilisateur__username', 'livre__titre']
