from django.urls import path
from .views import EventListView, EventListByDateView

urlpatterns = [
    path('events/', EventListView.as_view(), name='all-events'),
    path('events/<str:date>/', EventListByDateView.as_view(), name='events-by-date'),
]
