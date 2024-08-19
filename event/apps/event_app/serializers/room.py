from rest_framework import serializers
from event_app.models.room import Room


class RoomSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(max_length=100, required=True, allow_blank=True)
    adresse = serializers.CharField(max_length=10, required=True, allow_blank=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "nom",
            "adresse",
        ]
