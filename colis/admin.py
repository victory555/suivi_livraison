from django.contrib import admin
from .models import Colis
 
# Register your models here.
class ColisAdmin(admin.ModelAdmin):
    list_display=["numero_suivi","expediteur", "destinataire", "adresse","date_mise_a_jour"]
    search_fields=["numero_suivi","expediteur", "destinataire", "adresse"]
admin.site.register(Colis, ColisAdmin)