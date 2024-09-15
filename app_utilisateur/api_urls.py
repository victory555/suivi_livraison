from django.urls import path
from . import views

app_name = 'app_utilisateur'

urlpatterns = [
    path('get_user/', views.api_get_user, name="api_get_user"),
    path('get_colis/', views.api_get_colis, name="api_get_user"),
    path('get_livraison/', views.api_get_livraison, name="api_get_user"),

        
   
]
