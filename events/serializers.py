from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type','booking_open_window_start','booking_open_window_end','start_datetime','end_datetime']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        instance = super(EventSerializer, self).create(validated_data)
        return instance
