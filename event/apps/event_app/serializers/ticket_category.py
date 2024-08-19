from rest_framework import serializers
from event_app.models.ticket_category_1 import Ticket_category_1


class TicketcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_category_1
        fields = [
            "id",
            "title",
            "price",
            "event",
            "description",
        ]
