from rest_framework import serializers
from .models import *

class RestaurantSerializer(serializers.ModelSerializer):
   owner = serializers.ReadOnlyField(source='owner.id')
   
   class Meta:
        model = Restaurant
        read_only_fields=('slug', 'owner')
        fields = (
            'id',
            'name',
            'slug',
            'owner'
        )
                  