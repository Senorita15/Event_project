from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.apps.event_app.serializers import TicketcategorySerializer
from event.apps.event_app.models import Ticket_category_1
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from datetime import date
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, action


class category_creation_form(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role=='gerant':
            serializer = TicketcategorySerializer()
            context = {"serializer": serializer}
            return render(request, "event_app/ticket_category/add.html", context)
        return HttpResponse("YOU ARE NOT AUTHORIZED TO ACCESS THIS PAGE")


class category_edit_form(View):
    def get(self, request, pk=None):
        if request.user.is_authenticated:
            connected_user = request.user
            created_by_connected_user = Ticket_category_1.objects.filter(
                created_by=connected_user
            )
            try:
                category = get_object_or_404(created_by_connected_user, pk=pk)
                serializer = TicketcategorySerializer(instance=category)
                context = {"serializer": serializer, "category": category}
                return render(request, "event_app/ticket_category/edit.html", context)
            except:
                return HttpResponse(
                    "THE REQUESTED EVENT DOESNT EXIST OR YOU ARE NOT THE AUTHOR OF ITS CREATION"
                )
        return HttpResponse("YOU ARE NOT AUTHORIZED TO ACCESS THIS PAGE")


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_authenticated:
            user_connected = request.user
            queryset = Ticket_category_1.objects.filter(created_by=user_connected)
            serializer_class = TicketcategorySerializer(queryset, many=True)
            return Response(
                serializer_class.data,
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        data = request.data.copy()
        serializer = TicketcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = serializer.errors
        context = {"message": message}
        return Response(context, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            user_connected = request.user
            queryset = Ticket_category_1.objects.filter(created_by=user_connected)
            try:
                event = get_object_or_404(queryset, pk=pk)
                serializer = TicketcategorySerializer(event)
                content = {"data": serializer.data}
                return Response(content)
            except:
                message = "THE REQUESTED EVENT DOESNT EXIST OR YOU ARE NOT THE AUTHOR OF ITS CREATION"
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                queryset = Ticket_category_1.objects.all()
                event = get_object_or_404(queryset, pk=pk)
                serializer = TicketcategorySerializer(event, data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    message = "ROOM SUCCESSFULLY UPDATED"
                    content = {"message": message, "data": serializer.data}
                    return Response(content, status=status.HTTP_200_OK)
                message = serializer.errors
                context = {"message": serializer.errors}
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
            except:
                message = "THE REQUESTED ROOM DOESNT EXIST OR YOU ARE NOT THE AUTHOR OF ITS CREATION"
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            try:
                user_connected = request.user
                queryset = Ticket_category_1.objects.filter(created_by=user_connected)
                room = get_object_or_404(queryset, pk=pk)
                room.delete()
                message = "EVENT SUCCESSFULLY DELETED"
                context = {"message": message}
                return Response(context, status=status.HTTP_200_OK)
            except:
                message = "THE REQUESTED EVENT DOESNT EXIST OR YOU ARE NOT THE AUTHOR OF ITS CREATION"
                return Response(
                    {"message": message}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)
