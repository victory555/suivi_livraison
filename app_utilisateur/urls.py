from django.urls import path
from . import views

app_name = 'app_utilisateur'

urlpatterns = [
    path('', views.login, name="login"),
    path('user/', views.connexion_view, name='user'),
    path('menu/', views.menu, name='menu'),
    path('index/', views.index, name='index'),
    path('utilisateurs/', views.menu, name='utilisateurs'),  # Assurez-vous que la vue correspondante est définie.
    path('user/add/', views.add_user, name='add_user'),
    path('ajouter_user/', views.ajouter_user, name='ajouter_user'),
    path('delete/<int:id>/', views.user_del, name='user_del'), 
    path('user/confirm_del/', views.delete_user, name='delete_user'),
    path('editer/<int:id>/', views.user_edit, name='user_edit'),
    path('profil/', views.profil, name='profil'),
    path('edit/<int:id>/', views.edit_user, name='edit_user'),
    
]
