from django.db import models
from restaurants.models import Restaurant
import uuid

class Tickets(models.Model):
    code=models.UUIDField(verbose_name="Tickets' code", default=uuid.uuid4,  primary_key=True)
    restaurant=models.ForeignKey(verbose_name="Restaurant", to=Restaurant, on_delete=models.PROTECT)
    name=models.CharField(verbose_name="Description", max_length=50)
    maxPurchaseCount=models.PositiveIntegerField(verbose_name="Maximum purchase count number")
    purchaseCount=models.PositiveIntegerField(verbose_name="Purchase count number")
    
    def __str__(self):
        return f'{self.name}({self.code})'

    class Meta:
        verbose_name="Ticket"
        verbose_name_plural="Tickets"

class PurchasedTickets(models.Model):
    id = models.AutoField(verbose_name="Purchase's ID", primary_key=True, auto_created=True)
    ticket=models.ForeignKey(verbose_name="Ticket", to=Tickets, on_delete=models.PROTECT)
    guestName=models.CharField(verbose_name="Guest's Name", max_length=100)

    def __str__(self):
        return f'{self.guestName}({self.ticket})'

    class Meta:
        verbose_name="Purchased ticket"
        verbose_name_plural="Purchased tickets"