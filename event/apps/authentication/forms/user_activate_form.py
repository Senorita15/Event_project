from django import forms
from event.apps.authentication.models import User
from django import forms
from django.utils import timezone


class Useractivate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["active"]
