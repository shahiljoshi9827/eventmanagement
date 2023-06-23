from django.shortcuts import render
from django.utils import timezone
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer


# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request":self.request})
        return context

    @action(methods=['GET'],detail=True)
    def summary(self, request, *args, **kwargs):
        instance = self.get_object()
        remaining_seats = instance.get_remaining_seats()

        booking_open = False
        now = timezone.now()
        if instance.booking_open_window_start <= now <= instance.booking_open_window_end:
            booking_open = True

        summary = {
            'event_id': instance.id,
            'event_title': instance.title,
            'total_seats': instance.max_seats,
            'remaining_seats': remaining_seats,
            'booking_open': booking_open,
            'booking_window': f"{instance.booking_open_window_start} - {instance.booking_open_window_end}",
        }
        return Response(summary, status=status.HTTP_200_OK)
