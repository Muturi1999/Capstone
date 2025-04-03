from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        """Test creating a user with all required fields"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_email_is_required(self):
        """Test that email is required for user creation"""
        with self.assertRaises(TypeError):
            User.objects.create_user(username='testuser', password='testpass123')

class TokenViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token_url = reverse('token_obtain_pair')
        
    def test_token_obtain(self):
        """Test obtaining a token with valid credentials"""
        response = self.client.post(
            self.token_url,
            {'username': 'testuser', 'password': 'testpass123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_token_invalid_credentials(self):
        """Test token is not created with invalid credentials"""
        response = self.client.post(
            self.token_url,
            {'username': 'testuser', 'password': 'wrongpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_token_missing_credentials(self):
        """Test token is not created with missing credentials"""
        response = self.client.post(
            self.token_url,
            {'username': 'testuser'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)