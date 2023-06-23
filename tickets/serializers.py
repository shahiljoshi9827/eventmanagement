from rest_framework import serializers
from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    # event = serializers.CharField(source="event.title")
    class Meta:
        model = Ticket
        fields = ['id', 'event','created_at']

