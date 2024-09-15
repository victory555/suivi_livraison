from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Utilisateur(AbstractUser):
    date_creation = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    # Ajout des related_name pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Changez le related_name ici
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Changez le related_name ici
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username