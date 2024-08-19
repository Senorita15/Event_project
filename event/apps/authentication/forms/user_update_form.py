from django.contrib.auth.forms import UserChangeForm
from event.apps.authentication.models import User
from django import forms
from django.utils import timezone


class Userchange(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "genre",
            "email",
            "username",
            "dob",
            "genre",
            "telephone",

        ]
        widgets = {
            "dob": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sélectionner une date",
                    "type": "date",
                    "min": (timezone.now() - timezone.timedelta(days=16*365)).date(),
                    "max": timezone.now().date(),
                },
                format="%Y-%m-%d",
            )
        }
