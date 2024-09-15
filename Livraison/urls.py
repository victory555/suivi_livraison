from django.urls import path
from . import views

app_name='Livraison'
urlpatterns = [
    path('', views.login, name="login"),
    path('menu/', views.menu, name='menu'),  # Assurez-vous que le nom est unique
    path('add_Livraison/', views.add_Livraison, name='add_Livraison'),
    path('ajouter_Livraison/', views.ajouter_Livraison, name='ajouter_Livraison'),
    path('delete/<int:id>/', views.Livraison_del, name='Livraison_del'), 
    path('Livraison/confirm_del/', views.delete_Livraison, name='delete_Livraison'),
    path('editer/<int:id>/', views.Livraison_edit, name='Livraison_edit'),
    path('edit/<int:id>/', views.edit_Livraison, name='edit_Livraison'), 
    
]