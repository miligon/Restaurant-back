"""
Module that holds the models for 'reservation' app
"""
import uuid
from django.db import models
from restaurants.models import Restaurant

class Tickets(models.Model):
    """ 
    Class that represents a ticket

    Attributes:
        code (UUID): Unique identifier for the ticket.
        restaurant (ForeignKey): The restaurant associated with the ticket.
        name (str): A brief description of the ticket.
        max_purchase_count (int): The maximum number of times this ticket can be purchased.
        purchase_count (int): The current purchase count for this ticket.
        soldout (bool): Indicates whether the ticket is sold out.

    Methods:
        __str__(): Returns a formatted string representation of the ticket.
        isSoldout(): Checks if the ticket is sold out.
        getAvailable(): Calculates the number of available tickets for purchase.

    """
    code = models.UUIDField(
        verbose_name="Tickets' code",
        default=uuid.uuid4,
        primary_key=True,
        blank=True)
    restaurant = models.ForeignKey(
        verbose_name="Restaurant",
        to=Restaurant,
        on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Description", max_length=50)
    max_purchase_count = models.PositiveIntegerField(
        verbose_name="Maximum purchase count number")
    purchase_count = models.PositiveIntegerField(
        verbose_name="Purchase count number")
    soldout = models.BooleanField(verbose_name="Sold Out", default=False)

    def __str__(self):
        return f'{self.name}({self.code})'

    def is_soldout(self):
        """
        Checks if the ticket is sold out based on the purchase count and maximum purchase count.

        Returns:
            bool: True if the ticket is sold out, False otherwise.
        """
        if self.purchase_count >= self.max_purchase_count:
            if not self.soldout:
                self.soldout = True
                self.save()
            return True
        else:
            if self.soldout:
                self.soldout = False
                self.save()
            return False

    def get_available(self):
        """
        Calculates the number of available tickets for purchase.

        Returns:
            int: The number of available tickets for purchase.
        """
        return self.max_purchase_count - self.purchase_count

    class Meta:
        """
        Defines extra data for the model like the name to show on the admin's page
        """
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"


class PurchasedTickets(models.Model):
    """
    Represents a purchased ticket by a guest.

    This class stores information about a purchased ticket, including a unique purchase ID,
    the associated ticket, guest's name, and the quantity of tickets purchased.

    Attributes:
        id (AutoField): Unique identifier for the purchase.
        ticket (ForeignKey): The ticket associated with this purchase.
        guest_name (str): The name of the guest who purchased the ticket.
        quantity (int): The quantity of tickets purchased.

    Methods:
        __str__(): Returns a formatted string representation of the purchased ticket.

    """
    id = models.AutoField(
        verbose_name="Purchase's ID",
        primary_key=True,
        auto_created=True)
    ticket = models.ForeignKey(
        verbose_name="Ticket",
        to=Tickets,
        on_delete=models.CASCADE)
    guest_name = models.CharField(verbose_name="Guest's Name", max_length=100)
    quantity = models.PositiveIntegerField(verbose_name="Quantity purchased")

    def __str__(self):
        return f'{self.guest_name}({self.ticket})'

    class Meta:
        """
        Defines extra data for the model like the name to show on the admin's page
        """
        verbose_name = "Purchased ticket"
        verbose_name_plural = "Purchased tickets"
