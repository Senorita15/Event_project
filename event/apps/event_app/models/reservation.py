from django.db import models
from event.apps.authentication.models.user import User
from .ticket_category_1 import Ticket_category_1
from django.utils import timezone
from phone_field import PhoneField


class Reservation(models.Model):

    genre=(
        ('Homme','H'),
        ('Femme','F') 
    )

    first_name = models.CharField(max_length=10,null=True,blank=True)
    last_name = models.CharField(max_length=10,null=True,blank=True)
    phone_number = PhoneField()
    email=models.EmailField()
    genre = models.CharField(max_length=10,choices=genre,verbose_name='Genre')
    ticket_event=models.ForeignKey(Ticket_category_1,null=True,blank=True,on_delete=models.SET_NULL)
    ticket_number=models.IntegerField(null=True,blank=True)
    validated = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    
    def __str__(self):
        return self.first_name+" "+self.last_name+""+self.ticket_event.event.name