from rest_framework import routers

from .viewsets import *

route = routers.SimpleRouter()
route.register('tickets', TicketViewSet)
route.register('purchase', PurchaseViewSet)

urlpatterns = route.urls