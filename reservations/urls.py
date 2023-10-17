"""
Module for URL routing using Django REST framework routers.

This module defines URL routing for endpoints:
- 'tickets' 
- 'purchase' endpoints 
"""
from rest_framework import routers

from .viewsets import TicketViewSet, PurchaseViewSet

route = routers.SimpleRouter()
route.register('tickets', TicketViewSet)
route.register('purchase', PurchaseViewSet)

urlpatterns = route.urls
