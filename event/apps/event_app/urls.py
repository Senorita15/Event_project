from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views.room import RoomViewSet, room_creation_form, room_edit_form

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room"),


urlpatterns = [
    # URLS ROOM
    path("room/create_form/", room_creation_form.as_view(), name="room_create_room"),
    path("room/edit_form/<int:pk>/", room_edit_form.as_view(), name="room-edit-form"),
    path(
        "room/update/<int:pk>/",
        RoomViewSet.as_view({"post": "update"}),
        name="room-update",
    ),
    path(
        "room/delete/<int:pk>/",
        RoomViewSet.as_view({"get": "destroy"}),
        name="room-destroy",
    ),
    path("", include(router.urls)),
]