from rest_framework import serializers
from .models import *

class PurchasedSerializer(serializers.ModelSerializer):
   class Meta:
        model = PurchasedTickets
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tickets
        fields = '__all__'
        