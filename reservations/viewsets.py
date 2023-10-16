from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.permissions import *
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import *
from .serializers import *
from .permissions import IsOwner

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self, *args,**kwargs):
        user = self.request.user
        if self.action == 'list':
            restaurant = self.request.query_params.get('restaurant', '')
            self.queryset = Tickets.objects.select_related('restaurant').filter(
                Q(restaurant__owner__exact=user)&
                Q(restaurant__slug__exact=restaurant)
                )
        return self.queryset
    
    def get_restaurant(self):
        restaurant_slug = self.request.data.get('restaurant', None)
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        # Check if the user is the owner of the restaurant
        if restaurant.owner != self.request.user:
            return False, Response({"error": "You can only create a ticket for your own restaurant."}, 
                            status=status.HTTP_403_FORBIDDEN)
        return True, restaurant
    
    def create(self, request, *args, **kwargs):
        # Get restaurant
        res, restaurant = self.check_restaurant()
        # If res is False -> restaurant is a Http Response 403
        if res == False: 
            return restaurant
        request.data['restaurant'] = restaurant.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        # Get restaurant
        res, restaurant = self.check_restaurant()
        # If res is False -> restaurant is a Http Response 403
        if res == False: 
            return restaurant
        request.data['restaurant'] = obj.id
        code = self.request.data.get('code', None)
        ticket = Tickets.objects.get(code=code)
        serializer = self.get_serializer(ticket,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PurchaseViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = PurchasedTickets.objects.all()
    serializer_class = PurchasedTicketsSerializer
    
    def retrieve(self, request,  *args, **kwarg):
        code = kwarg['pk']
        ticket = get_object_or_404(Tickets, code=code)
        serializer = TicketUnauthenticatedSerializer(ticket)
        return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            error_message = str(e)
            if "Trying to purchase more tickets than available!" in error_message:
                return Response(data={"error": error_message}, status=status.HTTP_403_FORBIDDEN)
            elif "Ticket is soldout!" in error_message:
                return Response(data={"error": error_message}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


