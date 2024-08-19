from django.contrib.auth.forms import PasswordChangeForm
from event.apps.authentication.models import User
from django import forms


class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = "__all__"
