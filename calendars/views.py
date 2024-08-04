from django.shortcuts import render
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from users.models import User
from reservation.models import Reservation
from condition.models import Condition

from .models import Event
from .serializers import EventSerializer, ConditionSerializer

from rest_framework.views import APIView
from rest_framework import status

class EventByDate(APIView):
    def get(self, request, username, date, format=None):
        try:
            if date is None:
                return JsonResponse({"message": "유효하지 않는 날짜 형식입니다. YYYY-MM-DD를 사용해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            
            # 사용자 객체 가져오기
            user = User.objects.get(username=username)

            # my_username 속 friends 필드의 다른 username을 가져온다
            friend_usernames = user.friends.values_list('username', flat=True)
            
            # 나+우리케어의 예약 정보 갖고와 json으로 변환
            appointment_data = []

            my_reservations = Reservation.objects.filter(client=user, date__date=date)
            appointment_data.extend([reservation.to_json() for reservation in my_reservations])

            for friend_username in friend_usernames:
                friend_reservations = Reservation.objects.filter(client__username=friend_username, date__date=date)
                appointment_data.extend([reservation.to_json() for reservation in friend_reservations])

            # 해당일의 식사 정보
            # meals = Meal.objects.filter(user=user, date=date)
            # 시리얼라이저

            # 해당일의 컨디션 정보
            condition = Condition.objects.filter(user=user, date=date).first()
            condition_serializer = ConditionSerializer(condition)

            # 시리얼라이져에 적용
            event = Event(
                date=date,
                user=user,
                appointment=appointment_data,
            )

            event_serializer = EventSerializer(event)

            return JsonResponse({
                "message": "조회에 성공하였습니다.",
                "result": {
                    **event_serializer.data,
                    "condition": condition_serializer.data,
                    # meal 시리얼라이저도 추가 필요
                }
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return JsonResponse({"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)
