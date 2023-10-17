"""
Module that contains some test cases for app 'reservations'
"""
import threading
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from restaurants.models import Restaurant
from .models import Tickets, PurchasedTickets


class ConcurrencyTicketPurchaseTest(APITestCase):
    """
    Test case for ticket purchase API, it uses Threads
    to simulate concurrency
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser_tickets', password='12345')
        self.user.save()

        self.restaurant = Restaurant(
            name="Restaurant TEST Ticket",
            owner=self.user)

        self.restaurant.save()

        # Create a ticket for testing
        ticket = Tickets.objects.create(
            name="Test Ticket",
            restaurant=self.restaurant,
            max_purchase_count=10,
            purchase_count=0,
            soldout=False
        )
        ticket.save()
        self.max_purchases = ticket.max_purchase_count
        self.code = str(ticket.code)

    def purchase_ticket(self, id, code, quantity):
        """ Function for simulating a ticket purchase """
        client = APIClient()
        for _ in range(quantity):
            try:
                data = {
                    "guest_name": "TestGuest",
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
        """ Create threads for concurrent ticket purchases """
        tickets_quantity = 6  # 12 intents
        threads_num = 2
        threads = []
        for i in range(threads_num):
            thread = threading.Thread(
                target=self.purchase_ticket,
                args=(i, self.code, tickets_quantity))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check the final state of the ticket after concurrent purchases
        ticket = Tickets.objects.get(code=self.code)
        self.assertEqual(ticket.purchase_count, self.max_purchases)
        self.assertEqual(ticket.get_available(), 0)  # Should be sold out

        # Check the total number of purchased tickets
        purchased_ticket_count = PurchasedTickets.objects.filter(
            ticket=ticket).count()
        self.assertEqual(purchased_ticket_count, self.max_purchases)


class TicketsTestCase(TestCase):
    """ Test Case for tickets """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser_tickets', password='12345')
        self.user.save()

        self.restaurant = Restaurant(
            name="Restaurant TEST Ticket",
            owner=self.user)

        self.restaurant.save()

        # Create a ticket for testing
        self.ticket = Tickets(
            restaurant=self.restaurant,
            name="10% OFF",
            max_purchase_count=5,
            purchase_count=0
        )

        self.ticket.save()

    def test_restaurant_shows_name_and_code(self):
        self.assertEqual(str(self.ticket), f"10% OFF({self.ticket.code})")

    def test_ticket_solds_out(self):
        """ Function for simulating a ticket purchase """
        client = APIClient()
        for i in range(self.ticket.max_purchase_count + 1):
            try:
                data = {
                    "guest_name": "TestGuest",
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
        self.assertEqual(ticket.purchase_count, self.ticket.max_purchase_count)
        self.assertEqual(ticket.get_available(), 0)  # Should be sold out

        # Check the total number of purchased tickets
        purchased_ticket_count = PurchasedTickets.objects.filter(
            ticket=ticket).count()
        self.assertEqual(
            purchased_ticket_count,
            self.ticket.max_purchase_count)
