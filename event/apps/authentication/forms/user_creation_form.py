from django.contrib.auth.forms import UserCreationForm
from event.apps.authentication.models import User
from django import forms
from django.utils import timezone


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "genre",
            "email",
            "username",
            "password1",
            "password2",
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
                    "max": (timezone.now() - timezone.timedelta(days=16 * 365))
                    .replace(year=timezone.now().year - 16)
                    .date(),
                },
                format="%Y-%m-%d",
            )
        }
