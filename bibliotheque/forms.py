from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Livre, Avis  # ← Ajoute Avis


class LivreForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier un livre"""

    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'description', 'categorie', 'fichier_pdf', 'couverture']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription personnalisé"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# À la fin du fichier :
class AvisForm(forms.ModelForm):
    """Formulaire pour ajouter un avis"""

    class Meta:
        model = Avis
        fields = ['note', 'commentaire']
        widgets = {
            'note': forms.RadioSelect(),
            'commentaire': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Partagez votre avis sur ce livre...'
            }),
        }