from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Profile
from utils import UrlUtils

class ProfileViewTestCase(APITestCase):

    def test_create_profile(self):
        url = reverse(UrlUtils.PROFILE_CREATE)
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '+911234567890',
            'username': 'johndoe'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().first_name, 'John')

    def test_update_profile(self):
        profile = Profile.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            phone_number='9876543210',
            username='janedoe'
        )
        url = reverse(UrlUtils.PROFILE_GET_OR_UPDATE, args=[profile.id])
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone_number': '+911234567890',
            'username': 'updateduser'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.first_name, 'Updated')
