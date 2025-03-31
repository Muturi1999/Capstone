from django.urls import path, re_path
from .views import EventListCreateView, EventDetailView, SyncEventToGoogleView
from .views import BookEventView, CancelBookingView, JoinWaitlistView
from .views import ListEventsView, FeedbackCreateView
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version="v1",
        description="API documentation for Event Management System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
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

    # swagger UI view
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),



]
