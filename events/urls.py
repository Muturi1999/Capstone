from django.urls import path
from .views import (
    EventListCreateView, EventDetailView, SyncEventToGoogleView,
    BookEventView, CancelBookingView, JoinWaitlistView,
    ListEventsView, FeedbackCreateView
)

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),

    # Booking & Waitlist URLs
    path('events/<int:event_id>/book/', BookEventView.as_view(), name='book-event'),
    path('events/<int:event_id>/cancel-booking/', CancelBookingView.as_view(), name='cancel-booking'),
    path('events/<int:event_id>/join-waitlist/', JoinWaitlistView.as_view(), name='join-waitlist'),

    # filtering api View
    path('events/', ListEventsView.as_view(), name='list-events'),
    # feedback apiview url
    path('events/<int:event_id>/feedback/', FeedbackCreateView.as_view(), name='event-feedback'),

    # syncing google calender 
    path('events/<int:event_id>/sync/', SyncEventToGoogleView.as_view(), name='sync-to-google'),
]
