from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import Http404
from django.views.generic import View
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash
from .forms import *
from event.apps.authentication.models import User
from django.utils.decorators import method_decorator


def user_create_form(request):
    form = UserForm()
    context = {"form": form}
    return render(request, "authentication/add_user.html", context)


def user_edit_form(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    form = Userchange(instance=user)
    context = {"form": form}
    return render(request, "authentication/edit_user.html", context)


# User_login_form
class LoginPageView(View):
    login_template = "authentication/login_user.html"

    def get(self, request):
        return render(request, "authentication/login_user.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                return redirect("user-list")
            else:
                messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
                return redirect("login")
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
            return redirect("login")



class UpdatepasswordView(View):
    def get(self, request):
        form = UpdatePasswordForm(request.user)
        context = {
            "form": form,
        }
        return render(request, "authentication/update_password_user.html", context)

    def post(self, request):
        assert isinstance(request, HttpRequest)
        form = UpdatePasswordForm(request.user, request.POST)
        assert isinstance(request, HttpRequest)
        if form.is_valid():
            user = User
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, "Votre mot de passe a été mis à jour avec succès!"
            )
            return redirect("login")
        else:
            messages.error(request, "Veuillez corriger l(es)'erreur(s)ci-dessous.")
            return redirect("login")
