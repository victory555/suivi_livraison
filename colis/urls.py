from django.urls import path
from . import views

app_name='colis'
urlpatterns = [
    path('', views.login, name="login"),
    path('menu/', views.menu, name='menu'),  # Assurez-vous que le nom est unique
    path('add_colis/', views.add_colis, name='add_colis'),
    path('ajouter_colis/', views.ajouter_colis, name='ajouter_colis'),
    path('delete/<int:id>/', views.colis_del, name='colis_del'), 
    path('colis/confirm_del/', views.delete_colis, name='delete_colis'),
    path('editer/<int:id>/', views.colis_edit, name='colis_edit'),
    path('edit/<int:id>/', views.edit_colis, name='edit_colis'), 
    
]