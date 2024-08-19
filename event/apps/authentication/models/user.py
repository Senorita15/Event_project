from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phone_field import PhoneField


class User(AbstractUser):

    genre = (("Homme", "H"), ("Femme", "F"))

    role = (("gerant", "gerant"), ("staff", "staff"))
    dob = models.DateTimeField(blank=True, null=True, verbose_name="Date de naissance")
    genre = models.CharField(max_length=10, choices=genre, verbose_name="Genre")
    telephone = PhoneField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=role, verbose_name="role")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        "authentication.User",
        max_length=100,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.first_name + " " + self.last_name
