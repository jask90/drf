import json

from django.contrib.auth.models import User
from hotels.models import *
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class InventoryTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')
        hotel = Hotel.objects.create(code='hotel_1', name='Hotel 1',)
        room = Room.objects.create(code='room_1', name='Room 1', hotel=hotel)
        rate = Rate.objects.create(code='rate_1', name='Rate 1', room=room)

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/api/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user
        self.hotel = hotel
        self.room = room
        self.rate = rate

    def test_create_intentory(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_inventory = {'name': 'Inventory 1', 'rate': 'rate_1', 'date': '2021-09-25', 'price': '35.67', 'quota': 2}

        response = client.post('/api/inventories/', test_inventory, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('rate', result)
        self.assertIn('date', result)
        self.assertIn('price', result)
        self.assertIn('quota', result)

        if 'id' in result:
            del result['id']

        self.assertEqual(result, test_inventory)

    def test_update_intentory(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        inventory = Inventory.objects.create(name='Inventory Update', rate=self.rate, date='2021-09-25', price=35.67, quota=2)

        test_inventory_update = {'name': 'Inventory Update', 'rate': 'rate_1', 'date': '2021-09-26', 'price': '15.67', 'quota': 1}

        response = client.put(f'/api/inventories/{inventory.id}/', test_inventory_update, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'id' in result:
            del result['id']

        self.assertEqual(result, test_inventory_update)

    def test_delete_intentory(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        inventory = Inventory.objects.create(name='Inventory Delete', rate=self.rate, date='2021-09-25', price=35.67, quota=2)

        response = client.delete(f'/api/inventories/{inventory.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        inventory_exists = Inventory.objects.filter(id=inventory.id)
        self.assertFalse(inventory_exists)

    def test_get_intentory(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_inventory = {'name': 'Inventory Get', 'rate': 'rate_1', 'date': '2021-09-24', 'price': '15.67', 'quota': 1}
        inventory = Inventory.objects.create(name=test_inventory['name'], rate=self.rate, date=test_inventory['date'], price=test_inventory['price'], quota=test_inventory['quota'])

        response = client.get(f'/api/inventories/{inventory.id}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'id' in result:
            del result['id']

        self.assertEqual(result, test_inventory)

    def test_list_inventory(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        Inventory.objects.create(name='Inventory List 1', rate=self.rate, date='2021-09-25', price=35.67, quota=2)
        Inventory.objects.create(name='Inventory List 2', rate=self.rate, date='2021-09-26', price=35.67, quota=2)

        response = client.get('/api/inventories/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(result), 2)

        for inventory in result:
            self.assertIn('id', inventory)
            self.assertIn('name', inventory)
            self.assertIn('rate', inventory)
            self.assertIn('date', inventory)
            self.assertIn('price', inventory)
            self.assertIn('quota', inventory)
