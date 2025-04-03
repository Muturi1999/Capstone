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
import io
import qrcode
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import io
import qrcode
from PIL import Image
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from reportlab.pdfgen import canvas
from .models import Event, Booking




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
    lookup_field = 'title'

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
    """Authenticated users can book an event and receive a PDF confirmation with a QR code."""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        event = Event.objects.get(id=event_id)

        if event.bookings.count() < event.capacity:
            booking = Booking.objects.create(user=request.user, event=event)

            # Generate QR code with booking details
            qr_data = f"Booking ID: {booking.id}, Event: {event.title}, User: {request.user.username}"
            qr = qrcode.make(qr_data)
            qr_io = io.BytesIO()
            qr.save(qr_io, format='PNG')
            qr_io.seek(0)

            # Convert BytesIO to an Image object and save as a temporary file
            qr_image = Image.open(qr_io)
            qr_image_path = "/tmp/temp_qr.png"
            qr_image.save(qr_image_path)

            # Generate PDF ticket
            pdf_io = io.BytesIO()
            p = canvas.Canvas(pdf_io)
            p.drawString(100, 800, f"Booking Confirmation for {event.title}")
            p.drawString(100, 780, f"Name: {request.user.username}")
            p.drawString(100, 760, f"Email: {request.user.email}")
            p.drawString(100, 740, f"Event Date: {event.date_time}")
            p.drawString(100, 720, f"Location: {event.location}")

            # Add QR code image to the PDF using its file path
            p.drawImage(qr_image_path, 100, 600, width=150, height=150)

            p.showPage()
            p.save()
            pdf_io.seek(0)

            # Send email with PDF attachment
            email = EmailMessage(
                subject=f"Booking Confirmed: {event.title}",
                body=f"Dear {request.user.username},\n\nYour booking for {event.title} has been confirmed.\nPlease find your ticket attached.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[request.user.email]
            )
            email.attach(f"Booking_{booking.id}.pdf", pdf_io.getvalue(), "application/pdf")
            email.send()

            return Response({"message": "Booking successful! Confirmation email sent."}, status=status.HTTP_201_CREATED)
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
