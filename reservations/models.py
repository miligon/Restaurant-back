from django.db import models
from restaurants.models import Restaurant

class Tickets(models.Model):
    code=models.UUIDField(verbose_name="Tickets' code", primary_key=True, auto_created=True)
    restaurant=models.ForeignKey(verbose_name="Restaurant", to=Restaurant, on_delete=models.PROTECT)
    name=models.CharField(verbose_name="Description", max_length=50)
    maxPurchaseCount=models.PositiveIntegerField(verbose_name="Maximum purchase count number")
    purchaseCount=models.PositiveIntegerField(verbose_name="Purchase count number")
    
    def __str__(self):
        return f'{self.name}({self.code})'

    class Meta:
        verbose_name="Ticket"
        verbose_name_plural="Tickets"