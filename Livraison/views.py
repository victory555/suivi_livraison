from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Livraison
from colis.models import Colis
from app_utilisateur.models import Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password


def add_Livraison(request):
    liste= Utilisateur.objects.all()
    colis=Colis.objects.all()
    return render(request, "Livraison/add_Livraison.html",{'liste':liste, 'colis':colis})
def ajouter_Livraison(request):
    livraison= Livraison.objects.all()
    if request.method == 'POST':
        # Récupération des données du formulaire
        colis_id = request.POST.get('colis')
        statut = request.POST.get('statut')
        destinataire_id = request.POST.get('destinataire')
    
 
        destinataire = get_object_or_404(Utilisateur, id=destinataire_id)
        colis = get_object_or_404(Colis, id=colis_id)

        new_Livraison = Livraison(colis=colis, statut=statut, proprietaire=destinataire)

        # Sauvegarde de l'Livraisonistrateur dans la base de données
        new_Livraison.save()

        # Redirection après la sauvegarde
        return redirect('Livraison:menu')  # Utilisez le nom de la vue défini dans `urls.py`

    return render(request, 'Livraison/add_Livraison.html', {'liste':Livraison})
def Livraison_del(request, id):
    livraison = get_object_or_404(Livraison, id=id)
    return render(request, "Livraison/delete_Livraison.html", {"Livraison": livraison})

def Livraison_edit(request, id):
    liste= Utilisateur.objects.all()
    colis=Colis.objects.all()
    livraison = get_object_or_404(Livraison, id=id)
    return render(request, "Livraison/edit_Livraison.html", {"Livraison": livraison,'liste':liste, 'colis':colis})

# views.py

def edit_Livraison(request, id):
    
    utilisateurs= Livraison.objects.all()
    livraison = get_object_or_404(Livraison, id=id)  # Récupération de l'Livraisonistrateur via son ID

    if request.method == 'POST':
        # Mettre à jour les informations de l'Livraisonistrateur
        colis_id = request.POST.get('colis')
        livraison.statut = request.POST.get('statut')
        destinataire_id = request.POST.get('destinataire')
    
 
        livraison.destinataire = get_object_or_404(Utilisateur, id=destinataire_id)
        livraison.colis = get_object_or_404(Colis, id=colis_id)

  # Assurez-vous que le modèle gère la modification du mot de passe de cette manière

        livraison.save()  # Sauvegarde les modifications
        return redirect(reverse('Livraison:menu'))  # Redirige vers une liste d'Livraison ou autre page

    
    return render(request, 'Livraison/menu.html', {"liste":utilisateurs})

def delete_Livraison(request):
    if request.method == "POST":
        id = request.POST.get('Livraison_id')  # Récupérer l'ID du formulaire
        livraison = get_object_or_404(Livraison, id=id)
        livraison.delete()  # Supprime l'Livraisonistrateur
        messages.success(request, "Livraison supprimé avec succès.")  # Message de confirmation
        return redirect('/Livraison/menu/')  # Redirige vers le menu ou une autre page
    return redirect('/Livraison/menu/')   



def menu(request):
    username = request.session.get('username')
    email = request.session.get('email')
    utilisateurs= Livraison.objects.all()
    nombre=utilisateurs.count()
    context={'username':username,'email':email, "liste":utilisateurs,"nombre":nombre}
    return render(request, 'Livraison/menu.html', context)
     


