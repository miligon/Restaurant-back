from rest_framework import serializers
from .models import *

class PurchasedTicketsSerializer(serializers.ModelSerializer):  
   class Meta:
        model = PurchasedTickets
        fields = '__all__'

#Serializer of tickets for unauthenticated users
class TicketUnauthenticatedSerializer(serializers.ModelSerializer):
   available = serializers.SerializerMethodField()
   class Meta:
        model = Tickets
        read_only_fields = ('soldout',)
        fields = (
            'code',
            'name',
            'available',
            'soldout'
            )
        
   def get_available(self, obj):
       return obj.getAvailable()
   
#Serializer of tickets for authenticated users
class TicketSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tickets
        read_only_fields = ('soldout',)
        fields = (
            'code',
            'restaurant',
            'name',
            'maxPurchaseCount',
            'purchaseCount',
            'soldout'
            )

        