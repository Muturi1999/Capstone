from django.urls import path
from .views import (
    EventListCreateView, EventDetailView, SyncEventToGoogleView,
    BookEventView, CancelBookingView, JoinWaitlistView,
    ListEventsView, FeedbackCreateView
)

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),

    # Booking & Waitlist URLs
    path('<int:event_id>/book/', BookEventView.as_view(), name='book-event'),
    path('<int:event_id>/cancel-booking/', CancelBookingView.as_view(), name='cancel-booking'),
    path('<int:event_id>/join-waitlist/', JoinWaitlistView.as_view(), name='join-waitlist'),

    # Filtering API View
    path('list/', ListEventsView.as_view(), name='list-events'),

    # Feedback API View
    path('<int:event_id>/feedback/', FeedbackCreateView.as_view(), name='event-feedback'),

    # Syncing Google Calendar
    path('<int:event_id>/sync/', SyncEventToGoogleView.as_view(), name='sync-to-google'),
]
