from django.urls import path
from . import views

app_name='perso_admin'
urlpatterns = [
    path('', views.login, name="login"),
    path('Admin/', views.connexion_view, name='Admin'),
    path('menu/', views.menu, name='menu'),  # Assurez-vous que le nom est unique
    path('dashboard/', views.dashboard, name='dashboard'),
    path('Admin/add_admin/', views.add_admin, name='add_admin'),
    path('ajouter_admin/', views.ajouter_admin, name='ajouter_admin'),
    path('delete/<int:id>/', views.admin_del, name='admin_del'), 
    path('admin/confirm_del/', views.delete_admin, name='delete_admin'),
    path('editer/<int:id>/', views.admin_edit, name='admin_edit'),
    path('edit/<int:id>/', views.edit_admin, name='edit_admin'), 
    path('logout/', views.logout, name='logout'),

    
]
