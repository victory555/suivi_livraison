from django.contrib import admin

# Register your models here.
from .models import Livraison
# Register your models here.
class LivraisonAdmin(admin.ModelAdmin):
    list_display=["colis", "statut", "date_derniere_mise_a_jour", "proprietaire"]
    search_fields=["colis", "statut", "proprietaire"]
admin.site.register(Livraison, LivraisonAdmin)