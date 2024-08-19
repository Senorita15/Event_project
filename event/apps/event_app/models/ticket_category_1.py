from django.db import models
from event.apps.authentication.models.user import User
from .event import Event


class Ticket_category_1(models.Model):
    title = models.CharField(max_length=10)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="created_by_ticket_category",
    )

    def __str__(self):
        return self.title + " " + self.event.name
