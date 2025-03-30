from rest_framework import serializers
from .models import Event, Booking, Waitlist, Feedback

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


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'event', 'booked_at']
        read_only_fields = ['user', 'booked_at']

    def validate(self, data):
        event = data['event']
        
        if Booking.objects.filter(user=self.context['request'].user, event=event).exists():
            raise serializers.ValidationError("You have already booked this event.")
        
        if event.bookings.count() >= event.capacity:
            raise serializers.ValidationError("Event is fully booked. You can join the waitlist instead.")

        return data

class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ['user', 'event', 'joined_at']
        read_only_fields = ['user', 'joined_at']

    def validate(self, data):
        event = data['event']
        
        if Booking.objects.filter(user=self.context['request'].user, event=event).exists():
            raise serializers.ValidationError("You are already booked for this event.")

        if Waitlist.objects.filter(user=self.context['request'].user, event=event).exists():
            raise serializers.ValidationError("You are already on the waitlist for this event.")

        return data

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'event', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']