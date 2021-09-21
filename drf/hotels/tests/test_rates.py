import json

from django.contrib.auth.models import User
from hotels.models import *
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RateTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')
        hotel = Hotel.objects.create(code='hotel_1', name='Hotel 1',)
        room = Room.objects.create(code='room_1', name='Room 1', hotel=hotel)

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/api/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user
        self.hotel = hotel
        self.room = room

    def test_create_rate(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_rate = {'code': 'room_1', 'name': 'Rate 1', 'room': 'room_1'}

        response = client.post('/api/rates/', test_rate, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', result)
        self.assertIn('name', result)
        self.assertIn('room', result)

        self.assertEqual(result, test_rate)

    def test_update_rate(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        rate = Rate.objects.create(code='rate_update', name='Rate Update', room=self.room)

        test_rate_update = {'code': 'rate_update', 'name': 'Rate Update 2', 'room': 'room_1'}

        response = client.put(f'/api/rates/{rate.code}/', test_rate_update, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, test_rate_update)

    def test_delete_rate(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        rate = Rate.objects.create(code='rate_delete', name='Rate Delete', room=self.room)

        response = client.delete(f'/api/rates/{rate.code}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        rate_exists = Rate.objects.filter(code=rate.code)
        self.assertFalse(rate_exists)

    def test_get_rate(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_rate = {'code': 'rate_get', 'name': 'Rate Get', 'room': 'room_1'}
        rate = Rate.objects.create(name=test_rate['name'], code=test_rate['code'], room=self.room)

        response = client.get(f'/api/rates/{rate.code}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, test_rate)

    def test_list_rates(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        Rate.objects.create(code='list_rate_1', name='List Rate 1', room=self.room)
        Rate.objects.create(code='list_rate_2', name='List Rate 2', room=self.room)

        response = client.get('/api/rates/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(result), 2)

        for rate in result:
            self.assertIn('code', rate)
            self.assertIn('name', rate)
            self.assertIn('room', rate)
