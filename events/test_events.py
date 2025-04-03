from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Event

User = get_user_model()

class EventTests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="TestPass123")
        
        # Login with the regular user
        self.client.login(username="user1", password="TestPass123")
        
        # Create an event
        self.event = Event.objects.create(
            title="Tech Conference", 
            description="A great tech event",
            location="Nairobi", 
            capacity=50, 
            date_time="2025-06-10T10:00:00Z",
            organizer=self.user
        )

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="admin", 
            email="admin@example.com", 
            password="password"
        )

    def test_list_events(self):
        """Test retrieving event list"""
        url = reverse('list-events')
        
        response = self.client.get(url, {'location': 'Nairobi'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_event(self):
        """Test booking an event"""
        url = reverse('book-event', args=[self.event.id])
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)