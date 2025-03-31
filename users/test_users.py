from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserAuthTests(APITestCase):

    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = reverse('token_obtain_pair')
        User.objects.create_user(username="testuser", password="TestPass123")
        data = {"username": "testuser", "password": "TestPass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
