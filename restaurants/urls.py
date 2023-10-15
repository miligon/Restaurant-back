from rest_framework import routers

from .viewsets import *

route = routers.SimpleRouter()
route.register('', RestarurantViewSet)

urlpatterns = route.urls   