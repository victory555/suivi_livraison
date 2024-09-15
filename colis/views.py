from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Colis
from Livraison.models import Livraison
from app_utilisateur.models import Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password


def add_colis(request):
    liste= Utilisateur.objects.all()
    return render(request, "colis/add_colis.html",{'liste':liste})
def ajouter_colis(request):
    colis= Colis.objects.all()
    if request.method == 'POST':
        # Récupération des données du formulaire
        numero_suivi = request.POST.get('numero_suivi')
        expediteur = request.POST.get('expediteur')
        destinataire_id = request.POST.get('destinataire')
        adresse = request.POST.get('adresse')
    
        if Colis.objects.filter(numero_suivi=numero_suivi).exists():
            messages.error(request, 'le numero de suivi existe déja')
            return render(request, 'colis/add_colis.html', {'error': "Le colis existe déja."})
        destinataire = get_object_or_404(Utilisateur, id=destinataire_id)
        new_colis = Colis(numero_suivi=numero_suivi, expediteur=expediteur, destinataire=destinataire,adresse=adresse)

        # Sauvegarde de l'colisistrateur dans la base de données
        new_colis.save()

        # Redirection après la sauvegarde
        return redirect('colis:menu')  # Utilisez le nom de la vue défini dans `urls.py`

    return render(request, 'colis/add_colis.html', {'liste':colis})
def colis_del(request, id):
    colis = get_object_or_404(Colis, id=id)
    return render(request, "colis/delete_colis.html", {"colis": colis})

def colis_edit(request, id):
    utilisateur= Utilisateur.objects.all()
    colis = get_object_or_404(Colis, id=id)
    return render(request, "colis/edit_colis.html", {"colis": colis,"liste":utilisateur})

# views.py

def edit_colis(request, id):
    
    utilisateurs= Colis.objects.all()
    colis = get_object_or_404(Colis, id=id)  # Récupération de l'colisistrateur via son ID

    if request.method == 'POST':
        # Mettre à jour les informations de l'colisistrateur
        colis.numero_suivi = request.POST.get('numero_suivi')
        colis.expediteur = request.POST.get('expediteur')
        destinataire_id = request.POST.get('destinataire')
        colis.adresse = request.POST.get('adresse')
        colis.destinataire = get_object_or_404(Utilisateur, id=destinataire_id)

  # Assurez-vous que le modèle gère la modification du mot de passe de cette manière

        colis.save()  # Sauvegarde les modifications
        return redirect(reverse('colis:menu'))  # Redirige vers une liste d'colis ou autre page

    
    return render(request, 'colis/menu.html', {"liste":utilisateurs})

def delete_colis(request):
    if request.method == "POST":
        id = request.POST.get('colis_id')  # Récupérer l'ID du formulaire
        colis = get_object_or_404(Colis, id=id)
        colis.delete()  # Supprime l'colisistrateur
        messages.success(request, "colis supprimé avec succès.")  # Message de confirmation
        return redirect('/colis/menu/')  # Redirige vers le menu ou une autre page
    return redirect('/colis/menu/')   



def menu(request):
    username = request.session.get('username')
    email = request.session.get('email')
    utilisateurs= Colis.objects.all()
    nombre=utilisateurs.count()
    context={'username':username,'email':email, "liste":utilisateurs,"nombre":nombre}
    return render(request, 'colis/menu.html', context)
     


