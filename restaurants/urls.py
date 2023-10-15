from rest_framework import routers

from .viewsets import *

route = routers.SimpleRouter()
route.register('', RestaurantViewSet)

urlpatterns = route.urls   