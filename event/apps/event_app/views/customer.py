from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import Http404
from django.views.generic import View
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash
from event.apps.authentication.forms import *
from event.apps.authentication.models import User
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from event.apps.authentication.models import User

def home(request):
    return render(request, "event_app/public/index.html")

def customer_create_form(request):
        form = UserForm()
        context = {"form": form}
        return render(request, "event_app/customer/sign_up.html", context)


def customer_edit_form(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    form = Userchange(instance=user)
    context = {"form": form}
    return render(request, "event_app/customer/edit.html", context)


#def user_activate(request, pk=None):
##    form = user_activate_form.Useractivate(instance=user)
#    context = {"form": form}
#    return render(request, "authentication/active_user.html", context)




class customer_UpdatepasswordView(View):
    def get(self, request):
        form = UpdatePasswordForm(request.user)
        context = {
            "form": form,
        }
        return render(request, "event_app/customer/edit_password.html", context)

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
class customer_Userviewsets(viewsets.ViewSet):

    renderer_classes = [TemplateHTMLRenderer]
    add_customer_template = "authentication/add_user.html"
    view_customer_template = "event_app/customer/view.html"

    # Create
    def list(self, request):
     
            queryset = User.objects.all()
            return redirect(
                "home"
            )
    
    def create(self, request):
        form = UserForm(data=request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "customer"
            user.save()
            messages.success(request, "record saved")
            return redirect("home")
        errors = form.errors
        messages.error(request, "Record not created. Errors: {}".format(errors))
        return HttpResponse(form.errors)

    # Retrieve
    def retrieve(self, request, pk=None):
        try:
            user = get_object_or_404(User, pk=pk)
            context = {"user": user}
            return Response(context, template_name=self.view_customer_template)
        except:
            message = "THE REQUESTED USER DOESNT EXIST"
        return HttpResponse({"message": message})

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
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return redirect("user-list")
        except:
            return HttpResponse("THIS ACCOUNT DOESN'T EXIST")

    @action(detail=False)
    def logout(self, request):
        logout(request)
        messages.info(request, "Déconnexion réussie")
        return redirect("login")


#class UserActivateView(View):
#    def post(self, request, pk=None):
#        user = get_object_or_404(User, pk=pk)
#        form = user_activate_form.Useractivate(data=request.POST, instance=user)
#        if form.is_valid():
#            form.save()
#            return redirect(
#                "user-list"
#            )  # Redirige vers la liste des utilisateurs après modification
#        return HttpResponse("Erreur lors de l'activation de l'utilisateur")
