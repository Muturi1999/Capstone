from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_date_time(self, value):
        """Ensure event is not in the past."""
        from django.utils.timezone import now
        if value < now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value
