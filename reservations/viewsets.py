from rest_framework import viewsets

from .models import *
from .serializers import *

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchasedTickets.objects.all()
    serializer_class = PurchasedTicketsSerializer    

