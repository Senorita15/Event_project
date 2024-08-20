from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.apps.event_app.serializers import (
    Reservation_public_serializer,
    Reservationserializer,
)
from event.apps.event_app.models import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from datetime import date
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, action
from django.core.mail import send_mail
from django.db.models import Func, IntegerField, Count


def queryset_to_list(queryset):
    liste = []
    for i in range(len(queryset)):
        liste.append(list(queryset[i].values())[0])
    return liste


class ExtractYear(Func):
    function = "Extract"
    template = "%(function)s(YEAR FROM %(expressions)s)"
    output_field = IntegerField()


class FilterReservationDataPage(View):
    def get(self, request):
        # Filter first names
        first_name_list = Reservation.objects.values_list(
            "first_name", flat=True
        ).distinct()
        # Filter last names
        last_name_list = Reservation.objects.values_list(
            "last_name", flat=True
        ).distinct()
        # Filter phone numbers
        phone_number_list = Reservation.objects.values_list(
            "phone_number", flat=True
        ).distinct()
        # Filter email addresses
        email_list = Reservation.objects.values_list("email", flat=True).distinct()
        # Filter genders
        gender_list = Reservation.objects.values_list("genre", flat=True).distinct()
        # Filter events
        events = Event.objects.filter(created_by=request.user)
        print(events)

        context = {
            "first_names": first_name_list,
            "last_names": last_name_list,
            "phone_numbers": phone_number_list,
            "emails": email_list,
            "genders": gender_list,
            "events": events,
        }

        return render(request, "event/reservation_templates/filter_page.html", context)


class FilteredReservationData(APIView):
    def post(self, request):
        selected_last_name = request.POST.get("last_name")
        selected_first_name = request.POST.get("first_name")
        selected_phone_number = request.POST.get("phone_number")
        print("allooooooooooooo", selected_phone_number)
        selected_email = request.POST.get("email")
        selected_event = request.POST.get("event")

        reservations = Reservation.objects.all()

        if selected_last_name:
            reservations = reservations.filter(last_name=selected_last_name)
        if selected_first_name:
            reservations = reservations.filter(first_name=selected_first_name)
        if selected_phone_number:
            reservations = reservations.filter(phone_number=selected_phone_number)
        if selected_email:
            reservations = reservations.filter(email=selected_email)
        if selected_event:
            reservations = reservations.filter(email=selected_event)

        serializer = Reservationserializer(reservations, many=True)

        context = {"data": serializer.data}

        return Response(context, status=status.HTTP_200_OK)


class ReservationViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_authenticated and request.user.role == "gerant":
            queryset = Reservation.objects.filter(
                ticket_event__event__created_by=request.user
            )
            if queryset:
                serializer_class = Reservationserializer(queryset, many=True)
                return Response(serializer_class.data, status=status.HTTP_200_OK)
            message = "NO TICKETS RELATED TO YOUR EVENT"
            context = {"message": message}
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        message = "YOUR ARE NOT AUTHORIZED TO ACCESS THIS PAGE"
        context = {"message": message}
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=["post"])
    def create_ticket(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)  # recuperation de l'evenement
        capacite = (
            event.limit_attendees
        )  # recuperation de la valeur du nombre total de participant prevu
        if not event:
            context = {
                "message": "NO EVENT CHOSEN",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = Reservationserializer(
            data=request.data
        )  # recuperation des donnees du formulaire
        if serializer.is_valid():
            # Récupérer les données valides du serializers
            data = serializer.validated_data
            # Récupérer les numéros de place disponible
            numeros_places_existants = Reservation.objects.filter(
                ticket_event__event=event
            ).values_list("ticket_number", flat=True)
            if numeros_places_existants.exists():
                # Affectation d'un numero de place parmi les places restantes
                num_place_disponible = next(
                    (
                        i
                        for i in range(1, capacite + 1)
                        if i not in numeros_places_existants
                    ),
                    None,
                )

                if num_place_disponible is None:
                    message = "THE EVENT IS ALREADY AT FULL CAPACITY"
                    print(message)
                    context = {
                        "message": message,
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                else:
                    # Creation d'un objet ticket
                    nouveau_ticket = Reservation.objects.create(
                        last_name=data.get("last_name"),
                        first_name=data.get("first_name"),
                        email=data.get("email"),
                        phone_number=data.get("phone_number"),
                        ticket_event=data.get("ticket_event"),
                        ticket_number=num_place_disponible,
                    )
                    nouveau_ticket.save()
                    ticket = nouveau_ticket
                    serializer = Reservationserializer(ticket)
                    message = "NEW TICKET CREATED"
                    context = {
                        "ticket": serializer.data,
                    }
                    return Response(context, status=status.HTTP_200_OK)

            else:
                num_place_disponible = 1
                nouveau_ticket = Reservation.objects.create(
                    last_name=data.get("last_name"),
                    first_name=data.get("first_name"),
                    email=data.get("email"),
                    phone_number=data.get("phone_number"),
                    ticket_event=data.get("ticket_event"),
                    ticket_number=num_place_disponible,
                )
                nouveau_ticket.save()
                ticket = Reservationserializer(nouveau_ticket)
                message = "NEW TICKET CREATED"
                context = {"ticket": ticket.data, "message": message}
                return Response(context, status=status.HTTP_200_OK)

        else:
            messages = serializer.errors
            context = {
                "messages": messages,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def reservation_validate(self, request, pk=None):
        if request.user.is_authenticated and request.user.role == "gerant":

            try:
                reservation = get_object_or_404(Reservation, pk=pk)
                queryset = Reservation.objects.filter(
                    ticket_event__event__created_by=request.user
                )
                reservation = queryset.filter(pk=reservation).first()
                if not reservation.validated:
                    reservation.validated = True
                    message = "RESERVATION SUCCESSFULLY UPDATED."
                    reservation.save()
                    # send_mail(
                    #    subject="CONFIRMATION DE RESERVATION DU TICKET",
                    #    from_email=None,
                    #    recipient_list=[reservation.email],
                    #    message = 'Salut, ' + reservation.last_name + '\nCongratulations, your ticket has been booked successfuly.\n' + reservation.ticket_event.event.name + '\n Ticket numero: ' + str(reservation.ticket_number),
                    #    fail_silently=False  )
                    # context={
                    #        'message': message
                    #    }
                    return Response(context, status=status.HTTP_200_OK)
                message = "RESERVATION AlREADY VALIDATED"
                context = {"message": message}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except:
                message = "TICKET NOT FOUND"
                context = {"message": message}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        message = "YOUR ARE NOT AUTHORIZED TO ACCESS THIS PAGE"
        context = {"message": message}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
