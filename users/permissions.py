from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Allows only Admin users to access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

class IsOrganizer(BasePermission):
    """Allows only Organizers to manage their own events."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_organizer()

    def has_object_permission(self, request, view, obj):
        # Enforced only event organizer can modify
        return obj.organizer == request.user  

class IsAttendee(BasePermission):
    """Allows only Attendees to book events."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_attendee()
