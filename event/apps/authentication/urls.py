from django.urls import path, include
from event.apps.authentication.views import (
    Userviewsets,
    user_create_form,
    user_edit_form,
    user_activate,
    LoginPageView,
    UpdatepasswordView,
    UserActivateView

)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"users", Userviewsets, basename="user"),


urlpatterns = [
    path("users/creation", user_create_form, name="user-form"),
    path("users/edit/<int:pk>/", user_edit_form, name="user-edit-form"),
    path("users/activateform/<int:pk>/", user_activate, name="user-activate-form"),
    path("login", LoginPageView.as_view(), name="login"),
    path("change_password/", UpdatepasswordView.as_view(), name="change_password"),
    path(
        "user/update/<int:pk>/",
        Userviewsets.as_view({"post": "update"}),
        name="user-update",
    ),
    path(
    "users/activate/<int:pk>/",
    UserActivateView.as_view(),
    name="user-activate",
    ),
    path("change_password/", UpdatepasswordView.as_view(), name="change_password"),
    path("", include(router.urls)),
]
