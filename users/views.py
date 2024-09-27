from django.core.exceptions import ValidationError
from datetime import datetime
import random

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.password_validation import validate_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserProfileSerializer, AcceptFriendRequestSerializer, FriendsListSerializer, DeleteFriendSerializer
from .models import User
from reservation.models import Reservation

from clinic.models import Clinic
from clinic.serializers import ClinicSerializer

# Create your views here.

# minseo : 회원 가입 뷰
class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        nickname = request.data.get('nickname')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        email = request.data.get('email')

        # 비밀번호 일치 확인
        if password != password2:
            return Response({"message": "입력한 비밀번호가 다릅니다."}, status = status.HTTP_400_BAD_REQUEST)
        
        # 비밀번호 유효성 검사
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"message": e.messages}, status = status.HTTP_400_BAD_REQUEST)

        # serializer로 유효성 검사 후 데이터 전달
        serializer = UserSerializer(data=request.data)
        serializer.email = email
        serializer.username = username
        serializer.nickname = nickname

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(password)
            user.save()

            return Response({"message": "회원가입에 성공하였습니다. "}, status = status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

# minseo : 로그인 뷰
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            auth_login(request, user) 
            return Response({"message": "로그인에 성공하였습니다. "}, status = status.HTTP_200_OK)
        else:
            return Response({"message": "이름 혹은 비밀번호가 잘못 입력 되었습니다. "}, status = status.HTTP_401_UNAUTHORIZED)

# minseo : 로그아웃 뷰
class LogoutView(APIView):
    def post(self, request):
        auth_logout(request)
        return Response({"message": "로그아웃에 성공하였습니다. "}, status = status.HTTP_200_OK)
    
# minseo : 탈퇴 뷰
class QuitView(APIView):
    def delete(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            user.delete()
            auth_logout(request) 
            return Response({"message": "탈퇴에 성공하였습니다. "}, status = status.HTTP_200_OK)
        else:
            return Response({"message": "이름 혹은 비밀번호가 잘못 입력 되었습니다. "}, status = status.HTTP_401_UNAUTHORIZED)
        
# minseo : 프로필 조회, 회원 정보 수정
class ProfileView(APIView):
    # 프로필 조회
    def get(self, request):
        try:
            username = request.GET.get('username')
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        

        serializer = UserProfileSerializer(user)
        user_data = serializer.data  

        if user.my_clinic:
            clinic = Clinic.objects.get(id=user.my_clinic.id)  
            clinic_data = ClinicSerializer(clinic).data
            user_data['my_clinic_name'] = clinic_data['name']
        else:
            user_data['my_clinic_name'] = None
        
        return Response({
            "message": "조회에 성공하였습니다.",
            "result": user_data
        }, status=status.HTTP_200_OK)

    
    # 회원 정보 수정
    def patch(self, request):
        username=request.data.get('username')
        try:
            user = User.objects.get(username=username)
            serializer = UserProfileSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "수정에 성공하였습니다. ",
                            "result" : serializer.data}, 
                            status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors,}, status = status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

# minseo : 우리 케어 친구 신청 기능
class FriendsView(APIView):
    def post(self, request):
        try:
            serializer = AcceptFriendRequestSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                friend_username = serializer.validated_data['friend_username']
                my_username = serializer.validated_data['my_username']
                try:
                    friend = User.objects.get(username=friend_username)
                    user = User.objects.get(username=my_username)
                except User.DoesNotExist:
                    return Response({"message": "사용자가 존재하지 않습니다.",}, status = status.HTTP_404_NOT_FOUND)
                
                user.friends.add(friend)
                friend.friends.add(user)
                
                return Response({"message": "우리 케어 친구가 추가되었습니다.",}, status = status.HTTP_200_OK)
            
            return Response({"message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)    
    
    def get(self, request):
        try:
            username = request.GET.get('username')
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FriendsListSerializer(user)

        friends_usernames = serializer.data.get('friends', [])  # Get the list of friends usernames or default to an empty list

        data = []
        for friends_username in friends_usernames:
            try:
                friend = User.objects.get(username=friends_username)
                data.append({friends_username: friend.nickname})
            except User.DoesNotExist:
                # Handle the case where the user does not exist, if necessary
                pass

        return Response({"message": "조회에 성공하였습니다.",
                        "result": data}, status=status.HTTP_200_OK)

    
    def delete(self, request):
        serializer = DeleteFriendSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            friend_username = serializer.validated_data['friend_username']
            my_username = serializer.validated_data['my_username']
            try:
                friend = User.objects.get(username=friend_username)
                user = User.objects.get(username=my_username)
            except User.DoesNotExist:
                return Response({"message": "사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            if friend in user.friends.all():
                user.friends.remove(friend)
                friend.friends.remove(user)
                return Response({"message": "우리 케어 친구가 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "이 사용자는 친구 목록에 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# 체질별 주의 사항
constitution_8_warning_message = {
    "목양" : ["와인은 줄여요!", "생선은 좋아요!"],
    "목음" : ["몸을 따뜻하게!", "차가운 음식은 NO!"],
    "토양" : ["매운 음식 주의!", "인삼은 맞지 않아요!!"],
    "토음" : ["항생제는 NO!", "자극적인 음식 NO!"],
    "금양" : ["바른 자세를 유지!", "간이 약해요"],
    "금음" : ["육식은 줄이기!", "생선은 좋아요!"],
    "수양" : ["겉을 시원하게!", "따뜻한 차 한잔!"],
    "수음" : ["차가운 음식은 NO!", "과식은 피해요"],    
}

# minseo : 친구 프로필 정보 불러오기
class FriendsProfileView(APIView):
    def get(self, request, username, format=None):
        try:
            # 오늘 날짜
            date = datetime.today().date()

            # 사용자 객체 가져오기
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"message": "사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

            # 내일부터 가장 가까운 예약 정보 가져오기
            closest_reservation = Reservation.objects.filter(client=user, date__date__gte=date).order_by('date').first()

            if closest_reservation:
                appointment_data = closest_reservation.to_json()
                appointment_clinic = appointment_data.get('client_my_clinic') 
                appointment_date = appointment_data.get('date')
            else:
                # 기본값 설정
                appointment_clinic = None
                appointment_date = None
            
            constitution = user.constitution_8
            if constitution in constitution_8_warning_message:
                warn_messages = constitution_8_warning_message[constitution]
                warn_message = random.choice(warn_messages)
            else:
                warn_message = ""

            return Response({
                "message": "조회에 성공하였습니다.",
                "result": {
                    "con_8": constitution,
                    "warn_message" : warn_message,
                    "reservation_clinic": appointment_clinic,
                    "reservation_datetime": appointment_date,
                }
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)
