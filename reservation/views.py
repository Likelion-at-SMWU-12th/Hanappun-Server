from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date


from .serializers import ReservationSerializer, ReservationCreateSerializer
from .models import Reservation

# Create your views here.

# minseo : 예약 CRUD 뷰셋
class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ReservationCreateSerializer
        return ReservationSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client']


# minseo : 예약 날짜로 예약 정보 조회
class ReservationByDateView(APIView):
    def get(self, request, date, format=None):
        try:
            from_date = parse_date(date)
            if from_date is None:
                return Response({"error": "유효하지 않는 날짜 형식입니다. YYYY-MM-DD를 사용해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            
            reservations = Reservation.objects.filter(date__date=from_date)
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

