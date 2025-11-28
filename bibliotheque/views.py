from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse, Http404
from .models import Livre, Favori
from .forms import LivreForm, CustomUserCreationForm


def accueil(request):
    """Page d'accueil avec les derniers livres et les plus téléchargés"""
    derniers_livres = Livre.objects.all()[:6]
    plus_telecharges = Livre.objects.order_by('-nombre_telechargements')[:6]

    context = {
        'derniers_livres': derniers_livres,
        'plus_telecharges': plus_telecharges,
    }
    return render(request, 'bibliotheque/accueil.html', context)


def catalogue(request):
    """Page catalogue avec recherche et filtres"""
    livres = Livre.objects.all()

    # Recherche
    query = request.GET.get('q')
    if query:
        livres = livres.filter(
            Q(titre__icontains=query) |
            Q(auteur__icontains=query) |
            Q(description__icontains=query)
        )

    # Filtre par catégorie
    categorie = request.GET.get('categorie')
    if categorie:
        livres = livres.filter(categorie=categorie)

    # Récupérer toutes les catégories pour le filtre
    categories = Livre.CATEGORIES

    context = {
        'livres': livres,
        'categories': categories,
        'query': query,
        'categorie_active': categorie,
    }
    return render(request, 'bibliotheque/catalogue.html', context)


def detail_livre(request, pk):
    """Page de détail d'un livre"""
    livre = get_object_or_404(Livre, pk=pk)
    est_favori = False

    if request.user.is_authenticated:
        est_favori = Favori.objects.filter(utilisateur=request.user, livre=livre).exists()

    context = {
        'livre': livre,
        'est_favori': est_favori,
    }
    return render(request, 'bibliotheque/detail_livre.html', context)


def lire_livre(request, pk):
    """Page pour lire un livre en ligne"""
    livre = get_object_or_404(Livre, pk=pk)

    # Incrémenter le compteur de lectures
    livre.nombre_lectures += 1
    livre.save()

    context = {
        'livre': livre,
    }
    return render(request, 'bibliotheque/lire_livre.html', context)


def telecharger_livre(request, pk):
    """Télécharger un livre PDF"""
    livre = get_object_or_404(Livre, pk=pk)

    # Incrémenter le compteur de téléchargements
    livre.nombre_telechargements += 1
    livre.save()

    try:
        return FileResponse(livre.fichier_pdf.open('rb'), as_attachment=True, filename=f"{livre.titre}.pdf")
    except FileNotFoundError:
        raise Http404("Le fichier n'existe pas")


@login_required
def ajouter_livre(request):
    """Page pour ajouter un livre"""
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save(commit=False)
            livre.ajoute_par = request.user
            livre.save()
            messages.success(request, 'Livre ajouté avec succès !')
            return redirect('detail_livre', pk=livre.pk)
    else:
        form = LivreForm()

    context = {
        'form': form,
    }
    return render(request, 'bibliotheque/ajouter_livre.html', context)


@login_required
def mes_livres(request):
    """Page listant les livres ajoutés par l'utilisateur"""
    livres = Livre.objects.filter(ajoute_par=request.user)

    context = {
        'livres': livres,
    }
    return render(request, 'bibliotheque/mes_livres.html', context)


@login_required
def modifier_livre(request, pk):
    """Page pour modifier un livre"""
    livre = get_object_or_404(Livre, pk=pk, ajoute_par=request.user)

    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livre modifié avec succès !')
            return redirect('detail_livre', pk=livre.pk)
    else:
        form = LivreForm(instance=livre)

    context = {
        'form': form,
        'livre': livre,
    }
    return render(request, 'bibliotheque/modifier_livre.html', context)


@login_required
def supprimer_livre(request, pk):
    """Supprimer un livre"""
    livre = get_object_or_404(Livre, pk=pk, ajoute_par=request.user)

    if request.method == 'POST':
        livre.delete()
        messages.success(request, 'Livre supprimé avec succès !')
        return redirect('mes_livres')

    context = {
        'livre': livre,
    }
    return render(request, 'bibliotheque/supprimer_livre.html', context)


@login_required
def favoris(request):
    """Page listant les favoris de l'utilisateur"""
    favoris = Favori.objects.filter(utilisateur=request.user)

    context = {
        'favoris': favoris,
    }
    return render(request, 'bibliotheque/favoris.html', context)


@login_required
def ajouter_favori(request, pk):
    """Ajouter un livre aux favoris"""
    livre = get_object_or_404(Livre, pk=pk)

    Favori.objects.get_or_create(utilisateur=request.user, livre=livre)
    messages.success(request, 'Livre ajouté aux favoris !')

    return redirect('detail_livre', pk=pk)


@login_required
def retirer_favori(request, pk):
    """Retirer un livre des favoris"""
    livre = get_object_or_404(Livre, pk=pk)

    Favori.objects.filter(utilisateur=request.user, livre=livre).delete()
    messages.success(request, 'Livre retiré des favoris !')

    return redirect('detail_livre', pk=pk)


@login_required
def profil(request):
    """Page de profil de l'utilisateur"""
    livres_ajoutes = Livre.objects.filter(ajoute_par=request.user).count()
    favoris_count = Favori.objects.filter(utilisateur=request.user).count()

    context = {
        'livres_ajoutes': livres_ajoutes,
        'favoris_count': favoris_count,
    }
    return render(request, 'bibliotheque/profil.html', context)


def inscription(request):
    """Page d'inscription"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue sur E-Biblio.')
            return redirect('accueil')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'bibliotheque/inscription.html', context)


def connexion(request):
    """Page de connexion"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} !')
                return redirect('accueil')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'bibliotheque/connexion.html', context)


def deconnexion(request):
    """Déconnexion de l'utilisateur"""
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('accueil')