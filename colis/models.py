from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from app_utilisateur.models import Utilisateur

class Colis(models.Model):
    numero_suivi = models.CharField(max_length=100, unique=True)
    expediteur = models.CharField(max_length=100)
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    adresse = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Colis {self.numero_suivi} de {self.expediteur} à {self.destinataire}"

    @staticmethod
    def ajouter_colis(numero_suivi, expediteur, destinataire, adresse):
        """
        Ajoute un nouveau colis à la base de données.
        """
        colis = Colis(
            numero_suivi=numero_suivi,
            expediteur=expediteur,
            destinataire=destinataire,
            adresse=adresse
        )
        colis.save()
        return colis

    def modifier_colis(self, expediteur=None, destinataire=None, adresse=None):
        """
        Modifie les informations du colis existant.
        """
        if expediteur:
            self.expediteur = expediteur
        if destinataire:
            self.destinataire = destinataire
        if adresse:
            self.adresse = adresse
        self.save()
        return self

    def supprimer_colis(self):
        """
        Supprime le colis de la base de données.
        """
        self.delete()
        return f"Colis {self.numero_suivi} supprimé avec succès."

    @staticmethod
    def consulter_colis(numero_suivi):
        """
        Consulter un colis par son numéro de suivi.
        """
        try:
            colis = Colis.objects.get(numero_suivi=numero_suivi)
            return colis
        except ObjectDoesNotExist:
            return None
