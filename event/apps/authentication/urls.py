from django.urls import path, include
from .views import (

    user_create_form,
    user_edit_form,
    LoginPageView,
    UpdatepasswordView,

)

urlpatterns = [
    path("users/creation", user_create_form, name="user-form"),
    path("users/edit/<int:pk>/", user_edit_form, name="user-edit-form"),
    path("login", LoginPageView.as_view(), name="login"),
    path("change_password/", UpdatepasswordView.as_view(), name="change_password"),
  

]
