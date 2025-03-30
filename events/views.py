from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import Event, Booking, Waitlist
from .serializers import EventSerializer, BookingSerializer, WaitlistSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin can see all users
        if self.request.user.is_staff:  
            return Event.objects.all()
        # enable organizers manage their own events
        return Event.objects.filter(organizer=self.request.user) 


class BookEventView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        user = self.request.user

        if event.bookings.count() < event.capacity:
            booking = serializer.save(user=user)
            
            # Sending confirmation email
            send_mail(
                subject=f"Booking Confirmed: {event.title}",
                message=f"You have successfully booked {event.title} on {event.date_time}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response({"message": "Booking successful!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)

class CancelBookingView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        event_id = kwargs['event_id']

        booking = Booking.objects.filter(user=user, event_id=event_id).first()
        if booking:
            booking.delete()

            # notifying first user in the waiting list
            first_waitlisted = Waitlist.objects.filter(event_id=event_id).order_by('joined_at').first()
            if first_waitlisted:
                first_waitlisted_user = first_waitlisted.user
                Booking.objects.create(user=first_waitlisted_user, event_id=event_id)
                first_waitlisted.delete()

                send_mail(
                    subject=f"Spot Opened for {booking.event.title}",
                    message=f"A spot has opened for {booking.event.title}, and you have been automatically booked.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[first_waitlisted_user.email],
                )

            return Response({"message": "Booking canceled."}, status=status.HTTP_200_OK)
        return Response({"error": "No booking found."}, status=status.HTTP_400_BAD_REQUEST)

class JoinWaitlistView(generics.CreateAPIView):
    serializer_class = WaitlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response({"message": "You have been added to the waitlist."}, status=status.HTTP_201_CREATED)