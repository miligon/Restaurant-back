"""
Module that contains the viewsets for the API endpoints of 'reservations' app
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from restaurants.models import Restaurant
from .models import Tickets, PurchasedTickets
from .serializers import *
from .permissions import IsOwner
from .signals import SoldOutError, TicketAvailableError


class TicketViewSet(viewsets.ModelViewSet):
    """
      A ViewSet for handling ticket-related operations.
    """
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if self.action == 'list':
            restaurant = self.request.query_params.get('restaurant', '')
            self.queryset = Tickets.objects.select_related('restaurant').filter(
                Q(restaurant__owner__exact=user) &
                Q(restaurant__slug__exact=restaurant)
            )
        return self.queryset

    def get_restaurant(self):
        """
        Retrieve restaurant object seacrhing by slug, it also
        checks if the restaurant's owner is the user
        """
        restaurant_slug = self.request.data.get('restaurant', None)
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        # Check if the user is the owner of the restaurant
        if restaurant.owner != self.request.user:
            return False, Response({
                "error": "You can only create a ticket for your own restaurant."
            },
                status=status.HTTP_403_FORBIDDEN)
        return True, restaurant

    def create(self, request, *args, **kwargs):
        # Get restaurant
        res, restaurant = self.get_restaurant()
        # If res is False -> restaurant is a Http Response 403
        if not res:
            return restaurant
        request.data['restaurant'] = restaurant.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Get restaurant
        res, restaurant = self.get_restaurant()
        # If res is False -> restaurant is a Http Response 403
        if not res:
            return restaurant
        request.data['restaurant'] = restaurant.id
        code = self.request.data.get('code', None)
        ticket = Tickets.objects.get(code=code)
        serializer = self.get_serializer(ticket, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PurchaseViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
      A ViewSet for handling purchase-related operations, only 
      retrieve and create operations are allowed.

      Retrive: returns information about ticket
      Create: creates new order
    """
    queryset = PurchasedTickets.objects.all()
    serializer_class = PurchasedTicketsSerializer

    def retrieve(self, request, *args, **kwarg):
        code = kwarg['pk']
        ticket = get_object_or_404(Tickets, code=code)
        serializer = TicketUnauthenticatedSerializer(ticket)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except SoldOutError as e:
            return Response(
                data={
                    "error": str(e)},
                status=status.HTTP_403_FORBIDDEN)
        except TicketAvailableError as e:
            return Response(
                data={
                    "error": str(e)},
                status=status.HTTP_403_FORBIDDEN)
        