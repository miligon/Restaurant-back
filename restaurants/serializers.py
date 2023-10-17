"""
Module that holds serializers for app 'restaurants'
"""
from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """ Serializer for Restaurant model. """
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Restaurant
        read_only_fields = ('slug', 'owner')
        fields = (
            'id',
            'name',
            'slug',
            'owner'
        )
