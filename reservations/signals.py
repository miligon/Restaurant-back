"""
Module that contains signals for app 'reservations'
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PurchasedTickets


@receiver(pre_save, sender=PurchasedTickets)
def purchased_ticket_created(sender, instance, **kwargs):
    """
    Signal receiver to handle the creation of purchased tickets.

    It checks if the ticket associated with the purchase is available for 
    purchase and updates the ticket's purchase count accordingly.
    """
    ticket = instance.ticket
    if ticket.get_available() <= 0:
        raise SoldOutError("Ticket is soldout!")
    else:
        if (ticket.get_available() - instance.quantity) < 0:
            raise TicketAvailableError("Trying to purchase more tickets than available!")
        ticket.purchase_count += instance.quantity
        ticket.save()
        # print('Ticket Sold!')

class SoldOutError(Exception):
    """Exception raised for sold out tickets."""

class TicketAvailableError(Exception):
    """Exception raised for ticket quantity exceeding available tickets."""
