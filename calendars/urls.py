from django.urls import path
from .views import get_calendar_events

urlpatterns = [
    path('calendars/events/', get_calendar_events, name='calendar-events'),
]
