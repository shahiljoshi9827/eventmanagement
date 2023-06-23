from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions, authentication, viewsets, status
from rest_framework.response import Response

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


# Create your views here.
class TicketViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.validated_data['event']

        # Check if booking window is open for the event
        now = timezone.now()
        if not (event.booking_open_window_start <= now <= event.booking_open_window_end):
            return Response({'error': 'Booking window is closed for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if maximum seats have been reached
        remaining_seats = event.max_seats - event.tickets.count()
        if remaining_seats <= 0:
            return Response({'error': 'Maximum seats for this event have been reached.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user = request.user
        tickets = Ticket.objects.filter(user=user).order_by('-created_at')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)