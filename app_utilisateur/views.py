from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Utilisateur
from colis.models import Colis
from Livraison.models import Livraison
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, get_object_or_404, redirect
from .models import Utilisateur  # Assurez-vous que ce modèle existe et contient les champs appropriés
from django.urls import reverse
from django.core import serializers


def index(request):
    username = request.session.get('username')
    email = request.session.get('email')
    user = get_object_or_404(Utilisateur, email=email)
    
    # Récupérer tous les colis associés à l'utilisateur
    colis = Colis.objects.filter(destinataire=user)
    
    # Récupérer toutes les livraisons associées à l'utilisateur
    livraisons = Livraison.objects.filter(proprietaire=user)
    
    return render(request, "app_utilisateur/index.html", {
        'username': username, 
        "email": email, 
        "user": user, 
        'colis': colis, 
        'livraisons': livraisons
    })

    
def profil(request):
    username = request.session.get('username')
    email = request.session.get('email')
    return render(request, "app_utilisateur/profil.html",{"username":username, "email":email})
def add_user(request):
    return render(request, "app_utilisateur/add_user.html")
def ajouter_user(request):
    administrateurs= Utilisateur.objects.all()
    if request.method == 'POST':
        # Récupération des données du formulaire
        user_name = request.POST.get('userName')
        user_email = request.POST.get('userEmail')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
    
        if Utilisateur.objects.filter(email=user_email).exists():
            messages.error(request, 'l\'email existe déja')
            return render(request, 'app_utilisateur/add_user.html', {'error': "L'email existe déja."})
        # Validation de la correspondance des mots de passe
        if password1 != password2:
            return render(request, 'app_utilisateur/add_user.html', {'error': "Les mots de passe ne correspondent pas."})

        # Hachage du mot de passe
        hashed_password = make_password(password1)

        # Création d'une instance de l'administrateur avec les données fournies
        new_user = Utilisateur(username=user_name, email=user_email, mot_de_passe=hashed_password)

        # Sauvegarde de l'useristrateur dans la base de données
        new_user.save()

        # Redirection après la sauvegarde
        return redirect('app_utilisateur:menu')  # Utilisez le nom de la vue défini dans `urls.py`

    return render(request, 'app_utilisateur/add_user.html', {'liste':administrateurs})
def user_del(request, id):
    user = get_object_or_404(Utilisateur, id=id)
    return render(request, "app_utilisateur/delete_user.html", {"user": user})

def user_edit(request, id):
    user = get_object_or_404(Utilisateur, id=id)
    return render(request, "app_utilisateur/edit_user.html", {"user": user})



def edit_user(request, id):
    # Récupération de l'utilisateur via son ID
    user = get_object_or_404(Utilisateur, id=id)
    utilisateur=Utilisateur.objects.all()
    if request.method == 'POST':
        # Mettre à jour les informations de l'utilisateur
        user.username = request.POST.get('userName')
        user.email = request.POST.get('userEmail')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Vérifier les mots de passe avant d'enregistrer
        if password1 and password1 == password2:
            user.mot_de_passe = make_password(password1)  # Hachage du mot de passe avant la sauvegarde

        # Sauvegarde des modifications
        user.save()
        # Redirige vers une autre vue après la modification
        return redirect(reverse('app_utilisateur:menu'))

    # En cas de requête GET, renvoie le formulaire avec l'utilisateur sélectionné
    return render(request, 'app_utilisateur/edit_user.html', {"liste": utilisateur})

def delete_user(request):
    if request.method == "POST":
        id = request.POST.get('user_id')  # Récupérer l'ID du formulaire
        user = get_object_or_404(Utilisateur, id=id)
        user.delete()  # Supprime l'useristrateur
        messages.success(request, "Administrateur supprimé avec succès.")  # Message de confirmation
        return redirect('/user/menu/')  # Redirige vers le menu ou une autre page
    return redirect('/user/menu/')   
def login(request):
    Administrateurs= Utilisateur.objects.all()
    return render(request, "app_utilisateur/login.html", {'administrateurs':Administrateurs})
def api_get_user(request):
    Utilisateurs= Utilisateur.objects.all()
    json_user= serializers.serialize("json",Utilisateurs )
    return HttpResponse(json_user)

def api_get_colis(request):
    colis= Colis.objects.all()
    json_colis= serializers.serialize("json",colis )
    return HttpResponse(json_colis)

def api_get_livraison(request):
    livraisons= Livraison.objects.all()
    json_livraisons= serializers.serialize("json",livraisons )
    return HttpResponse(json_livraisons)

def menu(request):
    username = request.session.get('username')
    email = request.session.get('email')
    utilisateurs= Utilisateur.objects.all()
    nombre=utilisateurs.count()
    context={'username':username,'email':email, "liste":utilisateurs,"nombre":nombre}
    return render(request, 'app_utilisateur/menu.html', context)
     

def connexion_view(request):
    Administrateurs= Utilisateur.objects.all()
    nombre=Administrateurs.count()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            administrateur = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
           messages.error(request, 'Email n\'existe pas') 
           return render(request, 'app_utilisateur/login.html')
        if administrateur is not None:
            if check_password(password, administrateur.mot_de_passe):
                request.session['username'] = administrateur.username
                request.session['email'] = administrateur.email
                request.session['nombre'] = nombre
                
                return redirect("app_utilisateur:index")
            else:
                messages.error(request, 'mot de passe incorrect')
    return render(request, 'app_utilisateur/login.html')


@login_required
def dashboard_view(request):
    return render(request, 'menu.html')

def ajouter_colis_view(request):
    if request.method == 'POST':
        numero_suivi = request.POST['numero_suivi']
        expediteur = request.POST['expediteur']
        destinataire = request.POST['destinataire']
        adresse = request.POST['adresse']
        Colis.ajouter_colis(numero_suivi, expediteur, destinataire, adresse)
        return redirect('colis_list')

    return render(request, 'ajouter_colis.html')

def modifier_colis_view(request, numero_suivi):
    colis = Colis.consulter_colis(numero_suivi)
    if request.method == 'POST':
        expediteur = request.POST['expediteur']
        destinataire = request.POST['destinataire']
        adresse = request.POST['adresse']
        colis.modifier_colis(expediteur, destinataire, adresse)
        return redirect('colis_detail', numero_suivi=colis.numero_suivi)

    return render(request, 'modifier_colis.html', {'colis': colis})

def supprimer_colis_view(request, numero_suivi):
    colis = Colis.consulter_colis(numero_suivi)
    if colis:
        colis.supprimer_colis()
    return redirect('colis_list')

