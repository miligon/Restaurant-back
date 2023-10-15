from rest_framework import viewsets

from .models import *
from .serializers import *

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer