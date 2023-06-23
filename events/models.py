from django.contrib.auth.models import User
from django.db import models

from tickets import models as ticket_models


class Event(models.Model):
    EVENT_TYPES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=7, choices=EVENT_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    max_seats = models.PositiveIntegerField(default=0)
    booking_open_window_start = models.DateTimeField()
    booking_open_window_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_remaining_seats(self):
        booked_seats = ticket_models.Ticket.objects.filter(event=self).count()
        remaining_seats = self.max_seats - booked_seats
        return remaining_seats


