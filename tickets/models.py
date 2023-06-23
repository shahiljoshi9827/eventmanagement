from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from events.models import Event


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add any additional fields you need for tickets

    def clean(self):
        if self.event.booking_open_window_start > timezone.now() or self.event.booking_open_window_end < timezone.now():
            raise ValidationError("Booking is not currently open for this event.")



    def __str__(self):
        return f"Ticket for {self.event.title} - {self.user.username}"
