from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.password_validation import validate_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserProfileSerializer, AcceptFriendRequestSerializer, FriendsListSerializer, DeleteFriendSerializer
from .models import User

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
        return Response({"message": "조회에 성공하였습니다.",
                        "result": serializer.data}, status=status.HTTP_200_OK)
    
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
        return Response({"message": "조회에 성공하였습니다.",
                        "result": serializer.data}, status=status.HTTP_200_OK)

    
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
