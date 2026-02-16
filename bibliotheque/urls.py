from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.accueil, name='accueil'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('livre/<int:pk>/', views.detail_livre, name='detail_livre'),
    path('livre/<int:pk>/lire/', views.lire_livre, name='lire_livre'),
    path('livre/<int:pk>/telecharger/', views.telecharger_livre, name='telecharger_livre'),

    # Gestion des livres
    path('ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('mes-livres/', views.mes_livres, name='mes_livres'),
    path('livre/<int:pk>/modifier/', views.modifier_livre, name='modifier_livre'),
    path('livre/<int:pk>/supprimer/', views.supprimer_livre, name='supprimer_livre'),

    # Favoris
    path('favoris/', views.favoris, name='favoris'),
    path('livre/<int:pk>/ajouter-favori/', views.ajouter_favori, name='ajouter_favori'),
    path('livre/<int:pk>/retirer-favori/', views.retirer_favori, name='retirer_favori'),

    # Profil
    path('profil/', views.profil, name='profil'),

    # Authentification
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # Avis (ajoute ces lignes)
    path('livre/<int:pk>/ajouter-avis/', views.ajouter_avis, name='ajouter_avis'),
    path('avis/<int:pk>/like/', views.liker_avis, name='liker_avis'),
    path('avis/<int:pk>/supprimer/', views.supprimer_avis, name='supprimer_avis'),
]