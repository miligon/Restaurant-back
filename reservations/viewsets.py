from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.permissions import *
from rest_framework.decorators import action

from django.db.models import Q

from .models import *
from .serializers import *
from .permissions import IsOwner

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        # Allow retrieve ticket detail to non authenticated users
        if self.action == 'retrieve' and not self.request.user.is_authenticated:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwner()]
    
    def get_queryset(self, *args,**kwargs):
        user = self.request.user
        if self.action == 'list':
            restaurant = self.request.query_params.get('restaurant', '')
            self.queryset = Tickets.objects.select_related('restaurant').filter(
                Q(restaurant__owner__exact=user)&
                Q(restaurant__id__exact=restaurant)
                )
        return self.queryset
    
    def get_serializer_class(self):
        # If the user is not authenticated show ticket detail with an special serializer
        if not self.request.user.is_authenticated:
            return TicketUnauthenticatedSerializer
        return TicketSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if the user is the owner of the restaurant
        restaurant_id = self.request.data.get('restaurant', None)
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        if restaurant.owner != request.user:
            return Response({"error": "You can only create a ticket for your own restaurant."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PurchaseViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = PurchasedTickets.objects.all()
    serializer_class = PurchasedTicketsSerializer

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


