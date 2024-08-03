from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from datetime import datetime

# View to list all events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# View to list events for a specific date
class EventListByDateView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            return Event.objects.filter(date=date_obj)
        except ValueError:
            return Event.objects.none()
