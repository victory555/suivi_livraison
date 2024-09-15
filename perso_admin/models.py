from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password


class Admin(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    email=models.EmailField()
    mot_de_passe=models.CharField(max_length=50)
    username=models.CharField(max_length=50)

    
    def __str__(self) -> str:
        return self.username
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def inscrire(self):
        # Logique pour inscrire un nouvel utilisateur
        pass

    def se_connecter(self):
        # Logique pour se connecter
        pass

    def mettre_a_jour_profil(self):
        # Logique pour mettre à jour le profil de l'utilisateur
        pass
