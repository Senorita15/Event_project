from rest_framework import serializers
from event.apps.event_app.models.event import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "limit_attendees",
            "room",
            "start_date",
            "end_date",
            "active",
            "description",
            "created_by",
        ]
