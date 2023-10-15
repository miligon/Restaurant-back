from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Tickets, PurchasedTickets

@receiver(pre_save, sender=PurchasedTickets)
def purchasedTicket_created(sender, instance, **kwargs):
    ticket = instance.ticket
    if ticket.isSoldout():
        raise Exception(f"Ticket {ticket.code} is soldout!")
    else:
        ticket.purchaseCount += 1
        ticket.save()
        ticket.isSoldout()
        ('Ticket Sold!')