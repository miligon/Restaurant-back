from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from restaurants.models import Restaurant

# Create your tests here.
class TicketsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_tickets', password='12345')
        self.user.save()

        self.restaurant = Restaurant(
            name="Restaurant TEST Ticket",
            owner=self.user)
        
        self.restaurant.save()

        self.ticket = Tickets(
            restaurant=self.restaurant,
            name="10% OFF",
            maxPurchaseCount=5,
            purchaseCount=3
            )
        
        self.ticket.save()

    def test_restaurant_shows_name_and_code(self):
        self.assertEqual(str(self.ticket), f"10% OFF({self.ticket.code})")
        