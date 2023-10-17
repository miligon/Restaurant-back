"""
Module for URL routing using Django REST framework routers.

This module defines URL routing for endpoints:
- 'restaurants'
"""
from rest_framework import routers
from .viewsets import RestaurantViewSet

route = routers.SimpleRouter()
route.register('', RestaurantViewSet)

urlpatterns = route.urls
