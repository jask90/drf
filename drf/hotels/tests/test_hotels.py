import json

from django.contrib.auth.models import User
from hotels.models import Hotel
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class HotelTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/api/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user

    def test_create_hotel(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_hotel = {'code': 'hotel_1', 'name': 'Hotel 1',}

        response = client.post('/api/hotels/', test_hotel, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('code', result)
        self.assertIn('name', result)

        self.assertEqual(result, test_hotel)

    def test_update_hotel(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        hotel = Hotel.objects.create(code='hotel_update', name='Hotel Update',)

        test_hotel_update = {'code': 'hotel_update','name': 'Hotel Update 2',}

        response = client.put(f'/api/hotels/{hotel.code}/', test_hotel_update, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, test_hotel_update)

    def test_delete_hotel(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        hotel = Hotel.objects.create(code='hotel_delete', name='Hotel Delete',)

        response = client.delete(f'/api/hotels/{hotel.code}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        hotel_exists = Hotel.objects.filter(code=hotel.code)
        self.assertFalse(hotel_exists)

    def test_get_hotel(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_hotel = {'code': 'hotel_get', 'name': 'Hotel Get',}
        hotel = Hotel.objects.create(name=test_hotel['name'], code=test_hotel['code'])

        response = client.get(f'/api/hotels/{hotel.code}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result, test_hotel)

    def test_list_hotels(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        Hotel.objects.create(code='list_hotel_1', name='List Hotel 1',)
        Hotel.objects.create(code='list_hotel_2', name='List Hotel 2',)

        response = client.get('/api/hotels/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(result), 2)

        for hotel in result:
            self.assertIn('code', hotel)
            self.assertIn('name', hotel)
