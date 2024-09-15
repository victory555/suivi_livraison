from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Admin
from colis.models import Colis
from Livraison.models import Livraison
from app_utilisateur.models import Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password

def add_admin(request):
    return render(request, "perso_admin/add_admin.html")
def ajouter_admin(request):
    Administrateurs= Admin.objects.all()
    if request.method == 'POST':
        # Récupération des données du formulaire
        admin_name = request.POST.get('adminName')
        admin_email = request.POST.get('adminEmail')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
    
        if Admin.objects.filter(email=admin_email).exists():
            messages.error(request, 'l\'email existe déja')
            return render(request, 'perso_admin/add_admin.html', {'error': "L'email existe déja."})
        # Validation de la correspondance des mots de passe
        if password1 != password2:
            return render(request, 'perso_admin/add_admin.html', {'error': "Les mots de passe ne correspondent pas."})

        # Hachage du mot de passe
        hashed_password = make_password(password1)

        # Création d'une instance de l'administrateur avec les données fournies
        new_admin = Admin(username=admin_name, email=admin_email, mot_de_passe=hashed_password)

        # Sauvegarde de l'administrateur dans la base de données
        new_admin.save()

        # Redirection après la sauvegarde
        return redirect('perso_admin:menu')  # Utilisez le nom de la vue défini dans `urls.py`

    return render(request, 'perso_admin/add_admin.html', {'liste':Administrateurs})
def admin_del(request, id):
    admin = get_object_or_404(Admin, id=id)
    return render(request, "perso_admin/delete_admin.html", {"admin": admin})

def dashboard(request):
    administrateurs= Admin.objects.all()
    utilisateurs= Utilisateur.objects.all()
    colis= Colis.objects.all()
    livraison= Livraison.objects.all()
    nb_admin=administrateurs.count()
    nb_user=utilisateurs.count()
    nb_colis=colis.count()
    nb_livraison=livraison.count()
    donnees={'administrateurs':administrateurs,"utilisateurs":utilisateurs,'colis':colis,"livraison":livraison, 'nb_admin':nb_admin ,'nb_user':nb_user,"nb_colis":nb_colis,'nb_livraison':nb_livraison}
    return render(request, "perso_admin/dashboard.html", donnees)
def admin_edit(request, id):
    admin = get_object_or_404(Admin, id=id)
    return render(request, "perso_admin/edit_admin.html", {"admin": admin})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Admin  # Assurez-vous que ce modèle existe et contient les champs appropriés
from django.urls import reverse

def edit_admin(request, id):
    utilisateurs= Admin.objects.all()
    admin = get_object_or_404(Admin, id=id)  # Récupération de l'administrateur via son ID

    if request.method == 'POST':
        # Mettre à jour les informations de l'administrateur
        admin.username = request.POST.get('adminName')
        admin.email = request.POST.get('adminEmail')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password1 == password2:
            admin.mot_de_passe=make_password(password1)  # Assurez-vous que le modèle gère la modification du mot de passe de cette manière

        admin.save()  # Sauvegarde les modifications
        return redirect(reverse('perso_admin:menu'))  # Redirige vers une liste d'admin ou autre page

    
    return render(request, 'perso_admin/menu.html', {"liste":utilisateurs})

def delete_admin(request):
    if request.method == "POST":
        id = request.POST.get('admin_id')  # Récupérer l'ID du formulaire
        admin = get_object_or_404(Admin, id=id)
        admin.delete()  # Supprime l'administrateur
        messages.success(request, "Administrateur supprimé avec succès.")  # Message de confirmation
        return redirect('/admin/menu/')  # Redirige vers le menu ou une autre page
    return redirect('/admin/menu/')   
def login(request):
    Administrateurs= Admin.objects.all()
    return render(request, "perso_admin/login.html", {'administrateurs':Administrateurs})



def menu(request):
    username = request.session.get('username')
    email = request.session.get('email')
    utilisateurs= Admin.objects.all()
    nombre=utilisateurs.count()
    context={'username':username,'email':email, "liste":utilisateurs,"nombre":nombre}
    return render(request, 'perso_admin/menu.html', context)
     
def logout(request):
    request.session.flush()    
    return redirect(reverse("perso_admin:login"))

def connexion_view(request):
    Administrateurs= Admin.objects.all()
    nombre=Administrateurs.count()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            administrateur = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
           messages.error(request, 'Email n\'existe pas') 
           return render(request, 'perso_admin/login.html')
        if administrateur is not None:
            if check_password(password, administrateur.mot_de_passe):
                request.session['username'] = administrateur.username
                request.session['email'] = administrateur.email
                request.session['nombre'] = nombre
                
                return redirect("perso_admin:menu")
            else:
                messages.error(request, 'mot de passe incorrect')
    return render(request, 'perso_admin/login.html')


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

