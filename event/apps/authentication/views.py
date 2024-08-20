from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import Http404
from django.views.generic import View
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash
from .forms import *
from event.apps.authentication.models import User
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from event.apps.authentication.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def user_create_form(request):
    if request.user.is_authenticated:
        form = UserForm()
        context = {"form": form}
        return render(request, "authentication/add_user.html", context)
    return HttpResponseForbidden("YOU ARE NOT ALLOWED TO ACCESS THIS PAGE")


@login_required
def user_edit_form(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    form = Userchange(instance=user)
    context = {"form": form}
    return render(request, "authentication/edit_user.html", context)


def user_activate(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    form = user_activate_form.Useractivate(instance=user)
    context = {"form": form}
    return render(request, "authentication/active_user.html", context)


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
                if request.user.is_superuser:
                    return redirect("user-list")
                return redirect("home")
            else:
                messages.error(request, "Mauvais")
                return redirect("login")
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
            return redirect("login")


@method_decorator(login_required, name="dispatch")
class UpdatepasswordView(View):
    def get(self, request):
        form = UpdatePasswordForm(request.user)
        context = {
            "form": form,
        }
        return render(request, "authentication/update_password_user.html", context)

    def post(self, request):
        form = UpdatePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = User
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, "Votre mot de passe a été mis à jour avec succès!"
            )
            return redirect("login")
        else:
            print(form.errors)
            messages.error(request, "Veuillez corriger l(es)'erreur(s)ci-dessous.")
            return redirect("login")


# viewset for actions List, create, retrieve, update and destroy
@method_decorator(login_required, name="dispatch")
class Userviewsets(viewsets.ViewSet):

    renderer_classes = [TemplateHTMLRenderer]
    list_user_template = "authentication/list_user.html"
    add_user_template = "authentication/add_user.html"
    view_user_template = "authentication/view_user.html"

    # List
    def list(self, request):
        connected_user = request.user
        users = User.objects.all()
        context = {"users": users}
        return Response(context, template_name=self.list_user_template)

    # Create
    def create(self, request):
        form = UserForm(data=request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.created_by = request.user
            user.save()
            messages.success(request, "record saved")
            return redirect("user-list")
        errors = form.errors
        messages.error(request, "Record not created. Errors: {}".format(errors))
        return redirect("user-form")

    # Retrieve
    def retrieve(self, request, pk=None):
        user_connected = request.user
        queryset = User.objects.filter(created_by=user_connected)
        try:
            user = get_object_or_404(User, pk=pk)
            context = {"user": user}
            return Response(context, template_name=self.view_user_template)
        except:
            message = "THE REQUESTED USER DOESNT EXIST OR YOU ARE NOT THE AUTHOR OF ITS CREATION"
        return HttpResponse({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    # Update
    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        form = user_update_form.Userchange(data=request.data, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-list")
        return redirect("user-list")

    # destroy
    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect("user-list")

    @action(detail=False)
    def logout(self, request):
        logout(request)
        messages.info(request, "Déconnexion réussie")
        return redirect("login")


class UserActivateView(View):
    def post(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        form = user_activate_form.Useractivate(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(
                "user-list"
            )  # Redirige vers la liste des utilisateurs après modification
        return HttpResponse("Erreur lors de l'activation de l'utilisateur")
