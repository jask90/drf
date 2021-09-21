import json

from django.contrib.auth.models import User
from hotels.models import *
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RoomTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')
        hotel = Hotel.objects.create(code='hotel_1', name='Hotel 1',)

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/api/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user
        self.hotel = hotel

    def test_create_room(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_room = {'code': 'room_1', 'name': 'Room 1', 'hotel': 'hotel_1'}

        response = client.post('/api/rooms/', test_room, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', result)
        self.assertIn('name', result)
        self.assertIn('hotel', result)

        self.assertEqual(result, test_room)

    def test_update_room(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        room = Room.objects.create(code='room_update', name='Room Update', hotel=self.hotel)

        test_room_update = {'code': 'room_update', 'name': 'Room Update 2', 'hotel': 'hotel_1'}

        response = client.put(f'/api/rooms/{room.code}/', test_room_update, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, test_room_update)

    def test_delete_room(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        room = Room.objects.create(code='room_delete', name='Room Delete', hotel=self.hotel)

        response = client.delete(f'/api/rooms/{room.code}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        room_exists = Room.objects.filter(code=room.code)
        self.assertFalse(room_exists)

    def test_get_room(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_room = {'code': 'room_get', 'name': 'Room Get', 'hotel': 'hotel_1'}
        room = Room.objects.create(name=test_room['name'], code=test_room['code'], hotel=self.hotel)

        response = client.get(f'/api/rooms/{room.code}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, test_room)

    def test_list_rooms(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        Room.objects.create(code='list_room_1', name='List Room 1', hotel=self.hotel)
        Room.objects.create(code='list_room_2', name='List Room 2', hotel=self.hotel)

        response = client.get('/api/rooms/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(result), 2)

        for room in result:
            self.assertIn('code', room)
            self.assertIn('name', room)
            self.assertIn('hotel', room)
