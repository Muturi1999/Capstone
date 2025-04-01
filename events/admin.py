from django.contrib import admin
from .models import Event, Booking, Waitlist, Feedback

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location', 'organizer', 'capacity', 'recurring')
    search_fields = ('title', 'location', 'organizer__username')
    list_filter = ('recurring', 'date_time')
    ordering = ('-date_time',)

admin.site.register(Event, EventAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'booked_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('booked_at',)
    ordering = ('-booked_at',)

admin.site.register(Booking, BookingAdmin)

class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'joined_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('joined_at',)
    ordering = ('-joined_at',)

admin.site.register(Waitlist, WaitlistAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'created_at')
    search_fields = ('user__username', 'event__title', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Feedback, FeedbackAdmin)
