"""
Module that holds serializers for app 'reservations'
"""
from rest_framework import serializers
from .models import PurchasedTickets, Tickets


class PurchasedTicketsSerializer(serializers.ModelSerializer):
    """ Serializer for PurchasedTickets model. """
    class Meta:
        model = PurchasedTickets
        fields = '__all__'


class TicketUnauthenticatedSerializer(serializers.ModelSerializer):
    """
    Serializer for Tickets model intended to use with unauthorized users,
    only shows: code, name and available fields.
    """
    available = serializers.SerializerMethodField()

    class Meta:
        model = Tickets
        read_only_fields = ('available',)
        fields = (
            'code',
            'name',
            'available'
        )

    def get_available(self, obj):
        """ Returns the value of available tickets """
        return obj.get_available()


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for Tickets model, intended to use with authorized users
    for create/update tickets.
    """
    class Meta:
        model = Tickets
        read_only_fields = ('soldout',)
        fields = (
            'code',
            'restaurant',
            'name',
            'max_purchase_count',
            'purchase_count',
            'soldout'
        )
