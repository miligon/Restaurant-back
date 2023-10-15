from rest_framework import viewsets

from .models import *
from .serializers import *

class RestaurantViewSet(viewsets.ModelViewSet):
    #Change this to validate against user's 
    queryset = Restaurant.objects.filter(owner=1)
    serializer_class = RestaurantSerializer