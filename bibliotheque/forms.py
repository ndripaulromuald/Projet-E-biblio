from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Livre, Avis


class LivreForm(forms.ModelForm):

    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'description', 'categorie', 'fichier_pdf', 'couverture']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AvisForm(forms.ModelForm):

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