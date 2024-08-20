from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.apps.event_app.serializers import Reservation_public_serializer,Reservationserializer
from event.apps.event_app.models import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets 
from django.shortcuts import get_object_or_404
from datetime import date
from django.views.generic import View
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view, action



class reservation_creation_form(View):
        def get(self, request,pk=None):
            evenement = get_object_or_404(Event, pk=pk) #recuperation de l'objet evenement pour la vue 
            serializer=Reservation_public_serializer()
            context={
                'serializer':serializer,
                'evenement':evenement
            }
            return render (request,'event_app/public/add.html',context)
        


class ReservationViewSet_public(viewsets.ViewSet):
    
    renderer_classes = [TemplateHTMLRenderer]
    #evenement_add= 'event/public/add.html' #page de creation d'un ticket
    evenement_detail = 'event_app/public/add.html' #page de creation de vue d'un evenement
    evenement_list = 'event_app/public/index.html'   #liste des evenements visible sur la page d'acceuil
    #send_mail_page = 'app/client/send_mail.html'    #page d'affichage du message 

    #Endpoint_evenement_list
    def list(self, request, *args, **kwargs):
        evenements = Event.objects.filter(active=True) #filtrage des evenements actifs
        context = {'evenements': evenements}
        return Response(context, template_name=self.evenement_list)

    #Endpoint_evenement_detail
    def retrieve(self, request, pk=None):
        evenement = get_object_or_404(Event, pk=pk) #recuperation de l'objet evenement pour la vue 
        serializer = Reservation_public_serializer() #recuperation du serializer pour affichage du formulaire 
                                        #de reservation d'un ticket
        context = {
                   'evenement': evenement,
                   'serializer': serializer
                   }
        return Response(context, template_name=self.evenement_detail)
    
   