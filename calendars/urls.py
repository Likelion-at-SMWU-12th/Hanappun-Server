from django.urls import path
from .views import EventByDate, EventByMonth, EventOfToday

app_name='calendars'

urlpatterns = [
    path('event/detail/<str:username>/<str:date>/', EventByDate.as_view(), name='event-by-date'),
    path('event/month/<str:username>/<str:month>/', EventByMonth.as_view(), name='event-by-month'),
    path('event/today/<str:username>/', EventOfToday.as_view(), name='event-of-today'),
]
