from django.db import models
from event.apps.authentication.models.user import User
from django.utils import timezone


class Room(models.Model):
    nom = models.CharField(null=True, blank=True)
    adresse = models.CharField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nom
