from rest_framework import serializers
from event_app.models.reservation import Reservation

class Reservationserializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            'last_name',
            'first_name',
            'phone_number',
            'email',
            'ticket_event',
            'ticket_number',
            'validated',
            'created_at'
        ]