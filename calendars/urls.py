from django.urls import path
from .views import EventByDate, EventByMonth

app_name='calendars'

urlpatterns = [
    path('event/detail/<str:username>/<str:date>/', EventByDate.as_view(), name='event-by-date'),
    path('event/<str:username>/<str:month>/', EventByMonth.as_view(), name='event-by-month'),
]
