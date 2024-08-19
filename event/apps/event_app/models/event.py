from django.db import models
from event.apps.authentication.models.user import User
from .room import Room
from django.utils import timezone


class Event(models.Model):
    name = models.CharField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    limit_attendees = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="created_by_event",
    )

    def __str__(self):
        return self.name
