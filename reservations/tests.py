from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from restaurants.models import Restaurant

from rest_framework.test import APIClient, APITestCase
import threading

class ConcurrencyTicketPurchaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_tickets', password='12345')
        self.user.save()

        self.restaurant = Restaurant(
            name="Restaurant TEST Ticket",
            owner=self.user)
        
        self.restaurant.save()

        # Create a ticket for testing
        ticket = Tickets.objects.create(
            name="Test Ticket",
            restaurant=self.restaurant,
            maxPurchaseCount=10,
            purchaseCount=0,
            soldout=False
        )
        ticket.save()
        self.maxPurchases = ticket.maxPurchaseCount
        self.code = str(ticket.code)

    def purchase_ticket(self, id, code, quantity):
        # Function for simulating a ticket purchase
        client = APIClient()
        for _ in range(quantity):  
            try:
                data = {
                        "guestName": "TestGuest",
                        "quantity": 1,
                        "ticket": code
                }
                response = client.post(
                    '/api/reservations/purchase/',
                    data=data,
                    format='json'
                )
                print(f"Thread {id}: {response.data}")
            except Exception as e:
                print(e)

    def test_concurrent_ticket_purchase(self):
        # Create threads for concurrent ticket purchases
        ticketsQuantity = 6 # 12 intents
        threadsNum = 2
        threads = []
        for i in range(threadsNum):
            thread = threading.Thread(
                target=self.purchase_ticket, 
                args=(i, self.code, ticketsQuantity))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check the final state of the ticket after concurrent purchases
        ticket = Tickets.objects.get(code=self.code)
        self.assertEqual(ticket.purchaseCount, self.maxPurchases)  
        self.assertEqual(ticket.getAvailable(), 0)  # Should be sold out

        # Check the total number of purchased tickets
        purchased_ticket_count = PurchasedTickets.objects.filter(ticket=ticket).count()
        self.assertEqual(purchased_ticket_count, self.maxPurchases)
        

class TicketsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_tickets', password='12345')
        self.user.save()

        self.restaurant = Restaurant(
            name="Restaurant TEST Ticket",
            owner=self.user)
        
        self.restaurant.save()

        # Create a ticket for testing
        self.ticket = Tickets(
            restaurant=self.restaurant,
            name="10% OFF",
            maxPurchaseCount=5,
            purchaseCount=0
            )
        
        self.ticket.save()

    def test_restaurant_shows_name_and_code(self):
        self.assertEqual(str(self.ticket), f"10% OFF({self.ticket.code})")

    def test_ticket_solds_out(self):
        # Function for simulating a ticket purchase
        client = APIClient()
        for i in range(self.ticket.maxPurchaseCount + 1):  
            try:
                data = {
                        "guestName": "TestGuest",
                        "quantity": 1,
                        "ticket": self.ticket.code
                }
                response = client.post(
                    '/api/reservations/purchase/',
                    data=data,
                    format='json'
                )
                print(f"Intento {i}: {response.data}")
            except Exception as e:
                print(e)

        # Check the final state of the ticket after purchases
        ticket = Tickets.objects.get(code=self.ticket.code)
        self.assertEqual(ticket.purchaseCount, self.ticket.maxPurchaseCount)  
        self.assertEqual(ticket.getAvailable(), 0)  # Should be sold out

        # Check the total number of purchased tickets
        purchased_ticket_count = PurchasedTickets.objects.filter(ticket=ticket).count()
        self.assertEqual(purchased_ticket_count, self.ticket.maxPurchaseCount)