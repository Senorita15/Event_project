from rest_framework import serializers
from event.apps.event_app.models.reservation import Reservation


class Reservation_public_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "last_name",
            "first_name",
            "phone_number",
            "email",
            "genre",
            "ticket_event",
        ]
