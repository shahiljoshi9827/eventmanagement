from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Event
from tickets import models

class EventAPITestCase(APITestCase):
    def setUp(self):
        # Create a test admin user
        self.admin_user = User.objects.create_superuser(username='admin', password='admin')

        # Create a test user
        self.user = User.objects.create_user(username='user', password='user123')

        # Create a test event
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            event_type='online',
            start_datetime='2023-06-01T10:00:00Z',
            end_datetime='2023-06-01T12:00:00Z',
            max_seats=100,
            booking_open_window_start='2023-05-30T00:00:00Z',
            booking_open_window_end='2023-06-01T00:00:00Z',
            created_by=self.admin_user
        )

    def test_create_event(self):
        # Ensure the admin user is authenticated
        self.client.force_authenticate(user=self.admin_user)

        # Send a POST request to create a new event
        data = {
            'title': 'New Event',
            'description': 'This is a new event',
            'event_type': 'offline',
            'start_datetime': '2023-07-01T10:00:00Z',
            'end_datetime': '2023-07-01T12:00:00Z',
            'max_seats': 50,
            'booking_open_window_start': '2023-06-30T00:00:00Z',
            'booking_open_window_end': '2023-07-01T00:00:00Z',
            'created_by': self.admin_user.id
        }
        response = self.client.post('/events/', data, format='json')

        # Ensure the response has a 201 CREATED status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the event was created successfully
        self.assertEqual(Event.objects.count(), 2)

    def test_book_ticket(self):
        # Ensure the user is authenticated
        self.client.force_authenticate(user=self.user)

        # Send a POST request to book a ticket for the event
        data = {
            'event': self.event.id,
            'user': self.user.id
        }
        response = self.client.post('/tickets/', data, format='json')


        # Ensure the response has a 201 CREATED status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the ticket was booked successfully
        self.assertEqual(models.Ticket.objects.count(), 1)
        self.assertEqual(models.Ticket.objects.first().event, self.event)

    def test_list_tickets(self):
        # Ensure the user is authenticated
        self.client.force_authenticate(user=self.user)

        # Send a GET request to list the tickets
        response = self.client.get('/tickets/')

        # Ensure the response has a 200 OK status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the tickets are listed correctly
        self.assertEqual(len(response.data), 0)

    # Add more test cases for other API endpoints

