from django.test import TestCase
from .models import *

# Create your tests here.
class restaurantsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()

        restaurant = Restaurant(
            name="Restaurant TEST 1",
            owner=self.user)
        
        restaurant.save()

        #Restaurant should augenerate its id
        self.restaurant = Restaurant.objects.get(pk=1)

    def test_restaurant_has_owner(self):
        self.assertEqual(self.restaurant.owner.username, "testuser")

    def test_restaurant_shows_name(self):
        self.assertEqual(str(self.restaurant), "Restaurant TEST 1")
        