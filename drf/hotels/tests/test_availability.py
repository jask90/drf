import json

from django.contrib.auth.models import User
from hotels.models import *
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class AvailabilityTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')
        hotel = Hotel.objects.create(code='hotel_1', name='Hotel 1',)
        room1 = Room.objects.create(code='room_1', name='Room 1', hotel=hotel)
        room2 = Room.objects.create(code='room_2', name='Room 2', hotel=hotel)
        room3 = Room.objects.create(code='room_3', name='Room 3', hotel=hotel)
        rate1 = Rate.objects.create(code='rate_1', name='Rate 1', room=room1)
        rate2 = Rate.objects.create(code='rate_2', name='Rate 1', room=room2)
        rate3 = Rate.objects.create(code='rate_3', name='Rate 1', room=room3)
        Inventory.objects.create(name='Inventory 1', rate=rate1, date='2021-09-25', price=15.17, quota=0)
        Inventory.objects.create(name='Inventory 2', rate=rate1, date='2021-09-26', price=15.27, quota=1)
        Inventory.objects.create(name='Inventory 3', rate=rate2, date='2021-09-25', price=25.37, quota=2)
        Inventory.objects.create(name='Inventory 4', rate=rate2, date='2021-09-26', price=25.47, quota=2)
        Inventory.objects.create(name='Inventory 5', rate=rate3, date='2021-09-25', price=35.57, quota=0)
        Inventory.objects.create(name='Inventory 6', rate=rate3, date='2021-09-26', price=35.67, quota=1)

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/api/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user
        self.hotel = hotel

    def test_create_availability(self):
        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)
        checkin_date = '2021-09-25'
        checkout_date = '2021-09-27'

        expected_response = {"rooms": [{"room_2": {"rates": [{"rate_2": {"breakdown": {"2021-09-25": {"price": "25.37", "quota": 2}, "2021-09-26": {"price": "25.47", "quota": 2}}, "total_price": "50.84"}}]}}]}

        response = client.get(f'/api/availability/{self.hotel.code}/{checkin_date}/{checkout_date}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, expected_response)
