from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views.room import RoomViewSet, room_creation_form, room_edit_form
from .views.event import EventViewSet, event_creation_form, event_edit_form

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room"),
router.register(r"events", EventViewSet, basename="event"),

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
    # URLS Events
    path(
        "event/status/<int:pk>/",
        EventViewSet.as_view({"get": "update_evenement_status"}),
        name="event-status",
    ),
    path("event/create_form/", event_creation_form.as_view(), name="event_create_room"),
    path(
        "event/edit_form/<int:pk>/", event_edit_form.as_view(), name="event-edit-form"
    ),
    path(
        "event/update/<int:pk>/",
        EventViewSet.as_view({"post": "update"}),
        name="event-update",
    ),
    path(
        "event/delete/<int:pk>/",
        EventViewSet.as_view({"get": "destroy"}),
        name="event-destroy",
    ),
    path("", include(router.urls)),
]
