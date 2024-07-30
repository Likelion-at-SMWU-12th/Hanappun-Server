from django.shortcuts import render
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserProfileSerializer
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
            return Response({"message": ["입력한 비밀번호가 다릅니다."]}, status=status.HTTP_400_BAD_REQUEST)
        
        # 비밀번호 유효성 검사
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"message": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # serializer로 유효성 검사 후 데이터 전달
        serializer = UserSerializer(data=request.data)
        serializer.email = email
        serializer.username = username
        serializer.nickname = nickname

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(password)
            user.save()

            return Response({"message":"회원가입에 성공하였습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
