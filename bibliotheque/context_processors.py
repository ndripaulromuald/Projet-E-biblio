from .models import Livre, Avis, Favori
from django.contrib.auth.models import User

def admin_stats(request):
    """Context processor pour ajouter les stats dans l'admin"""
    if request.path.startswith('/admin/'):
        return {
            'total_livres': Livre.objects.count(),
            'total_users': User.objects.count(),
            'total_avis': Avis.objects.count(),
            'total_favoris': Favori.objects.count(),
        }
    return {}