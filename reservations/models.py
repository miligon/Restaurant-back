from django.db import models
from restaurants.models import Restaurant
import uuid

class Tickets(models.Model):
    code=models.UUIDField(verbose_name="Tickets' code", default=uuid.uuid4,  primary_key=True, blank=True)
    restaurant=models.ForeignKey(verbose_name="Restaurant", to=Restaurant, on_delete=models.PROTECT)
    name=models.CharField(verbose_name="Description", max_length=50)
    maxPurchaseCount=models.PositiveIntegerField(verbose_name="Maximum purchase count number")
    purchaseCount=models.PositiveIntegerField(verbose_name="Purchase count number")
    soldout=models.BooleanField(verbose_name="Sold Out", default=False)
    
    def __str__(self):
        return f'{self.name}({self.code})'
    
    def isSoldout(self):
        if self.purchaseCount >= self.maxPurchaseCount:
            if self.soldout == False:
                self.soldout = True
                self.save()
            return True
        else:
            if self.soldout == True:
                self.soldout = False
                self.save()
            return False
    
    def getAvailable(self):
        return (self.maxPurchaseCount - self.purchaseCount)

    class Meta:
        verbose_name="Ticket"
        verbose_name_plural="Tickets"

class PurchasedTickets(models.Model):
    id = models.AutoField(verbose_name="Purchase's ID", primary_key=True, auto_created=True)
    ticket=models.ForeignKey(verbose_name="Ticket", to=Tickets, on_delete=models.CASCADE)
    guestName=models.CharField(verbose_name="Guest's Name", max_length=100)
    quantity = models.PositiveIntegerField(verbose_name="Quantity purchased")

    def __str__(self):
        return f'{self.guestName}({self.ticket})'

    class Meta:
        verbose_name="Purchased ticket"
        verbose_name_plural="Purchased tickets"