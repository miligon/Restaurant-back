"""
Module that holds configuration for app 'reservations'
"""
from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    """ Configuration class for the 'reservations' Django application. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    def ready(self):
        """
        Hook method called when the application is ready.

        This method imports the signals needed for the 'reservations' application.

        """
        import reservations.signals
