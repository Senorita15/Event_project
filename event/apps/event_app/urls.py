from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views.room import RoomViewSet, room_creation_form, room_edit_form
from .views.event import EventViewSet, event_creation_form, event_edit_form
from .views.public import ReservationViewSet_public, reservation_creation_form
from .views.reservation import (
    ReservationViewSet,
    FilterReservationDataPage,
    FilteredReservationData,
)
from .views.ticket_category import (
    CategoryViewSet,
    category_creation_form,
    category_edit_form,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room"),
router.register(r"events", EventViewSet, basename="event"),
router.register(r"categories", CategoryViewSet, basename="category"),
router.register(r"reservations", ReservationViewSet, basename="reservation"),
router.register(r"home", ReservationViewSet_public, basename="events")


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
    # URLS Category
    path(
        "category/create_form/",
        category_creation_form.as_view(),
        name="category_create_",
    ),
    path(
        "category/edit_form/<int:pk>/",
        category_edit_form.as_view(),
        name="category-edit-form",
    ),
    path(
        "category/update/<int:pk>/",
        CategoryViewSet.as_view({"post": "update"}),
        name="category-update",
    ),
    path(
        "category/delete/<int:pk>/",
        CategoryViewSet.as_view({"get": "destroy"}),
        name="category-destroy",
    ),
    # URLS Reservation
    path("reservation/filter_page/", FilterReservationDataPage.as_view()),
    path(
        "reservation/create/<int:pk>/",
        ReservationViewSet.as_view({"post": "create_ticket"}),
        name="create_ticket",
    ),
    path(
        "reservation/validate/<int:pk>/",
        ReservationViewSet.as_view({"get": "reservation_validate"}),
        name="validate_reservation",
    ),
    # URLS Ticket
    path(
        "ticket/create_form/",
        reservation_creation_form.as_view(),
        name="reservation_create",
    ),
    path("", include(router.urls)),
]
