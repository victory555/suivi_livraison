from django.db import models
from colis.models import Colis
from app_utilisateur.models import Utilisateur
from django.core.exceptions import ObjectDoesNotExist


class StatutLivraison(models.TextChoices):
    EN_TRANSIT = 'in_transit', 'En Transit'
    LIVRE = 'delivered', 'Livré'
    RETARDE = 'delayed', 'Retardé'

class Livraison(models.Model):
    colis = models.OneToOneField(Colis, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=StatutLivraison.choices, default=StatutLivraison.EN_TRANSIT)
    date_derniere_mise_a_jour = models.DateTimeField(auto_now=True)
    proprietaire=models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.colis.numero_suivi} - {self.statut}"

    @staticmethod
    def ajouter_livraison(colis, destinataire, statut):
        """
        Ajoute un nouveau livraison à la base de données.
        """
        livraison = Livraison(
            colis=colis,
            proprietaire=destinataire,
            statut=statut
        )
        livraison.save()
        return livraison

    def modifier_livraison(self, expediteur=None, destinataire=None, adresse=None):
        """
        Modifie les informations du livraison existant.
        """
        if expediteur:
            self.expediteur = expediteur
        if destinataire:
            self.destinataire = destinataire
        if adresse:
            self.adresse = adresse
        self.save()
        return self

    def supprimer_livraison(self):
        """
        Supprime le livraison de la base de données.
        """
        self.delete()
        return f"livraison {self.id} supprimé avec succès."

    @staticmethod
    def consulter_livraison(id):
        """
        Consulter un livraison par son numéro de suivi.
        """
        try:
            livraison = Livraison.objects.get(id=id)
            return livraison
        except ObjectDoesNotExist:
            return None
