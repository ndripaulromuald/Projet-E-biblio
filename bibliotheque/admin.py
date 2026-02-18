from django.contrib import admin
from .models import Livre, Favori, Avis

admin.site.site_header = "E-Biblio Administration"
admin.site.site_title = "E-Biblio Admin"
admin.site.index_title = "Tableau de bord"

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

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['livre', 'utilisateur', 'note', 'date_creation', 'nombre_likes']
    list_filter = ['note', 'date_creation']
    search_fields = ['livre__titre', 'utilisateur__username', 'commentaire']
    readonly_fields = ['date_creation', 'date_modification']


