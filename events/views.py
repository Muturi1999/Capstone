# from rest_framework import generics, permissions, status, filters
# from rest_framework.response import Response
# from django.core.mail import send_mail
# from django.conf import settings
# from django_filters.rest_framework import DjangoFilterBackend
# from .pagination import EventPagination
# from .models import Event, Booking, Waitlist
# from .serializers import EventSerializer, BookingSerializer, WaitlistSerializer, FeedbackSerializer
# from users.permissions import IsAdmin, IsOrganizer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from .google_calendar import add_event_to_google_calendar


# class CreateEventView(generics.CreateAPIView):
#     """Only Admins & Organizers can create events."""
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOrganizer | IsAdmin]

#     def perform_create(self, serializer):
#         # setting organizer
#         serializer.save(organizer=self.request.user)


# class UpdateEventView(generics.UpdateAPIView):
#     """Only the event organizer can update their own event."""
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOrganizer]


# class DeleteEventView(generics.DestroyAPIView):
#     """Only Admin can delete events."""
#     queryset = Event.objects.all()
#     permission_classes = [permissions.IsAuthenticated, IsAdmin]


# class ListEventsView(generics.ListAPIView):
#     """Anyone can view events."""
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.AllowAny]


# class BookEventView(generics.CreateAPIView):
#     """Authenticated users can book an event."""
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         event = serializer.validated_data['event']
#         user = self.request.user

#         if event.bookings.count() < event.capacity:
#             booking = serializer.save(user=user)
            
#             # Sending confirmation email
#             send_mail(
#                 subject=f"Booking Confirmed: {event.title}",
#                 message=f"You have successfully booked {event.title} on {event.date_time}.",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[user.email],
#             )

#             return Response({"message": "Booking successful!"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"error": "Event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)


# class CancelBookingView(generics.DestroyAPIView):
#     """Authenticated users can cancel their booking."""
#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request, *args, **kwargs):
#         user = request.user
#         event_id = kwargs['event_id']

#         booking = Booking.objects.filter(user=user, event_id=event_id).first()
#         if booking:
#             booking.delete()

#             # Notifying first user in the waiting list
#             first_waitlisted = Waitlist.objects.filter(event_id=event_id).order_by('joined_at').first()
#             if first_waitlisted:
#                 first_waitlisted_user = first_waitlisted.user
#                 Booking.objects.create(user=first_waitlisted_user, event_id=event_id)
#                 first_waitlisted.delete()

#                 send_mail(
#                     subject=f"Spot Opened for {booking.event.title}",
#                     message=f"A spot has opened for {booking.event.title}, and you have been automatically booked.",
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[first_waitlisted_user.email],
#                 )

#             return Response({"message": "Booking canceled."}, status=status.HTTP_200_OK)
#         return Response({"error": "No booking found."}, status=status.HTTP_400_BAD_REQUEST)


# class JoinWaitlistView(generics.CreateAPIView):
#     """Authenticated users can join the waitlist if an event is full."""
#     serializer_class = WaitlistSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#         return Response({"message": "You have been added to the waitlist."}, status=status.HTTP_201_CREATED)
    

# class ListEventsView(generics.ListAPIView):
#     """List all events with filtering and pagination."""
#     queryset = Event.objects.all().order_by('date_time')
#     serializer_class = EventSerializer
#     pagination_class = EventPagination

#     # Enable filtering and search
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['location', 'category'] 
#     search_fields = ['title', 'description']  


# class FeedbackCreateView(generics.CreateAPIView):
#     """Allows users to leave feedback for events."""
#     serializer_class = FeedbackSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class SyncEventToGoogleView(APIView):
#     """Manually sync an event to Google Calendar."""
#     permission_classes = [IsAuthenticated]

#     def post(self, request, event_id):
#         event = Event.objects.get(id=event_id)
#         event_link = add_event_to_google_calendar(event)
#         return Response({"message": "Event synced!", "calendar_link": event_link})
    

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import EventPagination
from .models import Event, Booking, Waitlist
from .serializers import EventSerializer, BookingSerializer, WaitlistSerializer, FeedbackSerializer
from users.permissions import IsAdmin, IsOrganizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .google_calendar import add_event_to_google_calendar


class EventListCreateView(generics.ListCreateAPIView):
    """Anyone can view events, but only Organizers/Admins can create."""
    queryset = Event.objects.all().order_by('date_time')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Only organizers or admins can create events."""
        if self.request.user.is_authenticated and (self.request.user.is_admin or self.request.user.is_organizer):
            serializer.save(organizer=self.request.user)
        else:
            return Response({"error": "You do not have permission to create an event."}, status=status.HTTP_403_FORBIDDEN)

class EventDetailView(generics.RetrieveAPIView):
    """Retrieve a single event by ID."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

class UpdateEventView(generics.UpdateAPIView):
    """Only the event organizer can update their own event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]


class DeleteEventView(generics.DestroyAPIView):
    """Only Admin can delete events."""
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class BookEventView(generics.CreateAPIView):
    """Authenticated users can book an event."""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        event = Event.objects.get(id=event_id)

        if event.bookings.count() < event.capacity:
            booking = Booking.objects.create(user=request.user, event=event)

            # Sending confirmation email
            send_mail(
                subject=f"Booking Confirmed: {event.title}",
                message=f"You have successfully booked {event.title} on {event.date_time}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )

            return Response({"message": "Booking successful!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)


class CancelBookingView(generics.DestroyAPIView):
    """Authenticated users can cancel their booking."""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs['event_id']
        return Booking.objects.filter(user=self.request.user, event_id=event_id).first()

    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking:
            booking.delete()

            # Notifying first user in the waiting list
            first_waitlisted = Waitlist.objects.filter(event_id=kwargs['event_id']).order_by('joined_at').first()
            if first_waitlisted:
                first_waitlisted_user = first_waitlisted.user
                Booking.objects.create(user=first_waitlisted_user, event_id=kwargs['event_id'])
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
    """Authenticated users can join the waitlist if an event is full."""
    serializer_class = WaitlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id)
        serializer.save(user=self.request.user, event=event)


class ListEventsView(generics.ListAPIView):
    """List all events with filtering and pagination."""
    queryset = Event.objects.all().order_by('date_time')
    serializer_class = EventSerializer
    pagination_class = EventPagination

    # Enable filtering and search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'category']
    search_fields = ['title', 'description']


class FeedbackCreateView(generics.CreateAPIView):
    """Allows users to leave feedback for events."""
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SyncEventToGoogleView(APIView):
    """Manually sync an event to Google Calendar."""
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        event_link = add_event_to_google_calendar(event)
        return Response({"message": "Event synced!", "calendar_link": event_link})
