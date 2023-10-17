"""
Module that holds configuration for app 'restaurants'
"""
from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    """ Configuration class for the 'restaurants' Django application. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'
