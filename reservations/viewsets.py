from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, mixins

from .models import *
from .serializers import *

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer

class PurchaseViewSet(mixins.CreateModelMixin, 
                  viewsets.GenericViewSet):
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


