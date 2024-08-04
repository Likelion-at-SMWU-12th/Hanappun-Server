from django.urls import path
from .views import EventByDate

app_name='calendars'

urlpatterns = [
    path('event/<str:username>/<str:date>/', EventByDate.as_view(), name='reservations-by-date'),
]
