"""
Module that contains the viewsets for the API endpoints of 'restaurants' app
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant
from .serializers import RestaurantSerializer
from .permissions import IsOwner


class RestaurantViewSet(viewsets.ModelViewSet):
    """
      A ViewSet for handling restaurant-related operations.
    """
    # Only owner
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        self.queryset = Restaurant.objects.filter(owner=user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
