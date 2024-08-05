from django.http import JsonResponse
from datetime import datetime, timedelta
import random

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
            try:
                condition = Condition.objects.get(user=user, date=date)
                condition_serializer = ConditionSerializer(condition).data
            except Condition.DoesNotExist:
                condition_serializer = None

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
                    "condition": condition_serializer,
                    # meal 시리얼라이저도 추가 필요
                }
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return JsonResponse({"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)

class EventByMonth(APIView):
    def get(self, request, username, month, format=None):
        try:
            if month is None:
                return JsonResponse({"message": "유효하지 않는 날짜 형식입니다. YYYY-MM를 사용해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                full_date_str = f"{month}-01"
                date = datetime.strptime(full_date_str, "%Y-%m-%d")
                start_date = date.replace(day=1)
                end_date = (date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            except ValueError:
                return JsonResponse({"message": "유효하지 않는 날짜 형식입니다. YYYY-MM을 사용해주세요."}, status=status.HTTP_400_BAD_REQUEST)

            # 사용자 객체 가져오기
            user = User.objects.get(username=username)

            # my_username 속 friends 필드의 다른 username을 가져온다
            friend_usernames = user.friends.values_list('username', flat=True)

            # response_data 초기화
            response_data = []
            current_date = start_date
            while current_date <= end_date:
                # 나의 예약이 있는지 확인
                my_reservations = Reservation.objects.filter(client=user, date__date=current_date)
                is_reservation = my_reservations.exists()
                # 우리케어 예약이 있는지 확인
                if(is_reservation == False):
                    for friend_username in friend_usernames:
                        friend_reservations = Reservation.objects.filter(client__username=friend_username, date__date=current_date)
                        if(friend_reservations.exists()):
                            is_reservation =True
                            break
                        
                # 컨디션 기록이 있는지 확인
                is_condition_or_meal = False
                condition = Condition.objects.filter(user=user, date=current_date).first()
                if condition != None:
                    # meal 기록이 있는지 확인   
                    # if meal 있으면 
                        # is_condition_or_meal = True
                    is_condition_or_meal = True

                # response_data에 데이터 추가
                response_data.append({
                    "date": current_date.strftime('%Y-%m-%d'),
                    "is_reservation": is_reservation,
                    "is_condition_or_meal": is_condition_or_meal,  
                })
                current_date += timedelta(days=1)

            return JsonResponse({
                "message": "조회에 성공하였습니다.",
                "result": response_data
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return JsonResponse({"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)

# 체질별 주의 사항
constitution_8_warning_message = {
    "목양" : ["와인은 줄여요!", "오늘은 생선 어때요?"],
    "목음" : ["몸을 따뜻하게 해요", "차가운 음식은 피해요"],
    "토양" : ["매운 음식 주의!", "인삼은 몸에 맞지 않아요!"],
    "토음" : ["항생제가 잘 맞지 않아요", "자극적인 음식은 줄여요"],
    "금양" : ["바른 자세를 유지해요", "간이 약해요"],
    "금음" : ["육식은 줄여요", "오늘은 생선 어때요?"],
    "수양" : ["겉을 시원하게 해요", "따뜻한 차 한잔 어때요?"],
    "수음" : ["차가운 음식은 안좋아요", "과식은 피해요"],    
}

class EventOfToday(APIView):
    def get(self, request, username, format=None):
        try:
            # 오늘 날짜
            date = datetime.today().date()

            # 사용자 객체 가져오기
            user = User.objects.get(username=username)
            # serializer = UserProfileSerializer(user)

            # 내일부터 가장 가까운 예약 정보 가져오기
            closest_reservation = Reservation.objects.filter(client=user, date__date__gte=date).order_by('date').first()

            if closest_reservation:
                appointment_data = closest_reservation.to_json()
            else:
                appointment_data = []

            # 해당일의 컨디션 정보
            try:
                condition = Condition.objects.get(user=user, date=date)
                condition_serializer = ConditionSerializer(condition).data
            except Condition.DoesNotExist:
                condition_serializer = None

            # 친구 목록
            friend_nickname = list(user.friends.values_list('nickname', flat=True))

            # 시리얼라이져에 적용
            event = Event(
                date=date,
                user=user,
                appointment=appointment_data,
            )

            event_serializer = EventSerializer(event)

            constitution = user.constitution_8
            if constitution in constitution_8_warning_message:
                warn_messages = constitution_8_warning_message[constitution]
                warn_message = random.choice(warn_messages)
            else:
                warn_message = ""


            return JsonResponse({
                "message": "조회에 성공하였습니다.",
                "result": {
                    **event_serializer.data,
                    "my_constitution_8" : user.constitution_8,
                    "warn_message" : warn_message,
                    "friend_usernames": friend_nickname,
                    "condition": condition_serializer,
                    # meal 시리얼라이저도 추가 필요
                }
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return JsonResponse({"11message": str(error)}, status=status.HTTP_400_BAD_REQUEST)
