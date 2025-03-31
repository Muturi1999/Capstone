from rest_framework import serializers
from .models import Event, Booking, Waitlist, Feedback
from django.utils.timezone import now

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'organizer', 'created_at']

    def validate_date_time(self, value):
        """Ensure event is not in the past."""
        if value < now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'booked_at']
        read_only_fields = ['id', 'user', 'booked_at']

    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to book an event.")

        user = request.user
        event = data['event']

        if Booking.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You have already booked this event.")
        
        if event.bookings.count() >= event.capacity:
            raise serializers.ValidationError("Event is fully booked. You can join the waitlist instead.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ['id', 'user', 'event', 'joined_at']
        read_only_fields = ['id', 'user', 'joined_at']

    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to join the waitlist.")

        user = request.user
        event = data['event']

        if Booking.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You are already booked for this event.")

        if Waitlist.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You are already on the waitlist for this event.")

        if event.bookings.count() < event.capacity:
            raise serializers.ValidationError("Event still has available spots. Please book instead of joining the waitlist.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'event', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
