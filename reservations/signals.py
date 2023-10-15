from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Tickets, PurchasedTickets

@receiver(pre_save, sender=PurchasedTickets)
def purchasedTicket_created(sender, instance, **kwargs):
    ticket = instance.ticket
    if ticket.isSoldout():
        raise Exception("Ticket is soldout!")
    else:
        if (ticket.getAvailable() - instance.quantity < 0):
            raise Exception("Trying to purchase more tickets than available!")
        ticket.purchaseCount += instance.quantity
        ticket.save()
        ticket.isSoldout()
        ('Ticket Sold!')

@receiver(pre_save, sender=Tickets)
def Ticket_save(sender, instance, **kwargs):
    instance.isSoldout()