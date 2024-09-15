from django.contrib import admin
from .models import Utilisateur

# Register your models here.
class UtilisateurAdmin(admin.ModelAdmin):
    list_display=["email", "username"]
    search_fields=["email", "username"]
admin.site.register(Utilisateur, UtilisateurAdmin)