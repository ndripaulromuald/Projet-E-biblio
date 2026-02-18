from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse, Http404
from .models import Livre, Favori, Avis
from .forms import LivreForm, CustomUserCreationForm, AvisForm


def accueil(request):
    derniers_livres = Livre.objects.all()[:6]
    plus_telecharges = Livre.objects.order_by('-nombre_telechargements')[:6]

    context = {
        'derniers_livres': derniers_livres,
        'plus_telecharges': plus_telecharges,
    }
    return render(request, 'bibliotheque/accueil.html', context)


def catalogue(request):
    livres = Livre.objects.all()

    query = request.GET.get('q')
    if query:
        livres = livres.filter(
            Q(titre__icontains=query) |
            Q(auteur__icontains=query) |
            Q(description__icontains=query)
        )

    categorie = request.GET.get('categorie')
    if categorie:
        livres = livres.filter(categorie=categorie)

    categories = Livre.CATEGORIES

    context = {
        'livres': livres,
        'categories': categories,
        'query': query,
        'categorie_active': categorie,
    }
    return render(request, 'bibliotheque/catalogue.html', context)


def detail_livre(request, pk):
    try:
        livre = get_object_or_404(Livre, pk=pk)
        est_favori = False
        mon_avis = None

        if request.user.is_authenticated:
            est_favori = Favori.objects.filter(utilisateur=request.user, livre=livre).exists()
            mon_avis = Avis.objects.filter(utilisateur=request.user, livre=livre).first()

        if mon_avis:
            autres_avis = livre.avis.exclude(pk=mon_avis.pk)
        else:
            autres_avis = livre.avis.all()

        context = {
            'livre': livre,
            'est_favori': est_favori,
            'mon_avis': mon_avis,
            'autres_avis': autres_avis,
        }
        return render(request, 'bibliotheque/detail_livre.html', context)

    except Exception as e:
        print(f"Erreur dans detail_livre: {e}")
        messages.error(request, "Erreur lors du chargement du livre.")
        return redirect('catalogue')
    

def lire_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    livre.nombre_lectures += 1
    livre.save()

    context = {
        'livre': livre,
    }
    return render(request, 'bibliotheque/lire_livre.html', context)


def telecharger_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    livre.nombre_telechargements += 1
    livre.save()

    try:
        return FileResponse(livre.fichier_pdf.open('rb'), as_attachment=True, filename=f"{livre.titre}.pdf")
    except FileNotFoundError:
        raise Http404("Le fichier n'existe pas")


@login_required
def ajouter_livre(request):
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
    livres = Livre.objects.filter(ajoute_par=request.user)

    context = {
        'livres': livres,
    }
    return render(request, 'bibliotheque/mes_livres.html', context)


@login_required
def modifier_livre(request, pk):
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
    favoris = Favori.objects.filter(utilisateur=request.user)

    context = {
        'favoris': favoris,
    }
    return render(request, 'bibliotheque/favoris.html', context)


@login_required
def ajouter_favori(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    Favori.objects.get_or_create(utilisateur=request.user, livre=livre)
    messages.success(request, 'Livre ajouté aux favoris !')

    return redirect('detail_livre', pk=pk)


@login_required
def retirer_favori(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    Favori.objects.filter(utilisateur=request.user, livre=livre).delete()
    messages.success(request, 'Livre retiré des favoris !')

    return redirect('detail_livre', pk=pk)


@login_required
def profil(request):
    livres_ajoutes = Livre.objects.filter(ajoute_par=request.user).count()
    favoris_count = Favori.objects.filter(utilisateur=request.user).count()

    context = {
        'livres_ajoutes': livres_ajoutes,
        'favoris_count': favoris_count,
    }
    return render(request, 'bibliotheque/profil.html', context)


def inscription(request):
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
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('accueil')


@login_required
def ajouter_avis(request, pk):
    try:
        livre = get_object_or_404(Livre, pk=pk)

        avis_existant = Avis.objects.filter(livre=livre, utilisateur=request.user).first()

        if request.method == 'POST':
            if avis_existant:
                form = AvisForm(request.POST, instance=avis_existant)
                message = 'Votre avis a été modifié avec succès !'
            else:
                form = AvisForm(request.POST)
                message = 'Merci pour votre avis !'

            if form.is_valid():
                avis = form.save(commit=False)
                avis.livre = livre
                avis.utilisateur = request.user
                avis.save()
                messages.success(request, message)
                return redirect('detail_livre', pk=pk)
        else:
            if avis_existant:
                form = AvisForm(instance=avis_existant)
            else:
                form = AvisForm()

        context = {
            'form': form,
            'livre': livre,
            'avis_existant': avis_existant,
        }
        return render(request, 'bibliotheque/ajouter_avis.html', context)

    except Exception as e:
        print(f"Erreur dans ajouter_avis: {e}")
        messages.error(request, "Erreur lors de l'ajout de l'avis.")
        return redirect('detail_livre', pk=pk)


@login_required
def liker_avis(request, pk):
    try:
        avis = get_object_or_404(Avis, pk=pk)

        if request.user in avis.likes.all():
            avis.likes.remove(request.user)
        else:
            avis.likes.add(request.user)

        return redirect('detail_livre', pk=avis.livre.pk)

    except Exception as e:
        print(f"Erreur dans liker_avis: {e}")
        messages.error(request, "Erreur lors du like.")
        return redirect('catalogue')


@login_required
def supprimer_avis(request, pk):
    try:
        avis = get_object_or_404(Avis, pk=pk, utilisateur=request.user)
        livre_pk = avis.livre.pk

        if request.method == 'POST':
            avis.delete()
            messages.success(request, 'Votre avis a été supprimé.')
            return redirect('detail_livre', pk=livre_pk)

        context = {
            'avis': avis,
        }
        return render(request, 'bibliotheque/supprimer_avis.html', context)

    except Exception as e:
        print(f"Erreur dans supprimer_avis: {e}")
        messages.error(request, "Erreur lors de la suppression.")
        return redirect('catalogue')