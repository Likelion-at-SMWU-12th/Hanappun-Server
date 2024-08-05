# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import Condition
from .serializers import ConditionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

# Condition 기록 생성 뷰
class ConditionCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_username = request.data.get('user')
        user = get_object_or_404(User, username=user_username)
        data = request.data.copy()
        data['user'] = user  # minseo : 해당 user 모델 연결
        
        serializer = ConditionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "컨디션 기록이 생성되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Condition 기록 조회 뷰
class ConditionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        conditions = Condition.objects.all()
        serializer = ConditionSerializer(conditions, many=True)
        return Response({"message": "컨디션 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)

# # Condition 기록 수정 뷰
# class ConditionUpdateView(APIView):
#     permission_classes = [AllowAny]

#     def put(self, request, pk):
#         condition = get_object_or_404(Condition, pk=pk)
#         user_username = request.data.get('user')
#         user = get_object_or_404(User, username=user_username)
#         data = request.data.copy()
#         data['user'] = user  # 사용자 이름을 ID로 변환
        
#         serializer = ConditionSerializer(condition, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "컨디션 기록이 수정되었습니다.", "data": serializer.data}, status=status.HTTP_200_OK)
#         return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# # Condition 기록 삭제 뷰
# class ConditionDeleteView(APIView):
#     permission_classes = [AllowAny]

#     def delete(self, request, pk):
#         condition = get_object_or_404(Condition, pk=pk)
#         condition.delete()
#         return Response({"message": "컨디션 기록이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 특정 날짜의 Condition 기록 조회 뷰
class ConditionByDateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username, date):
        conditions = Condition.objects.filter(date=date, user=username)
        serializer = ConditionSerializer(conditions, many=True)
        return Response({"message": "특정 날짜의 컨디션 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request,username, date):
        conditions = Condition.objects.filter(date=date)
        if not conditions.exists():
            return Response({"message": "해당 날짜에 대한 컨디션 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        user_username = request.data.get('user')
        user = get_object_or_404(User, username=user_username)
        data = request.data.copy()
        data['user'] = user  # 사용자 이름을 ID로 변환

        response_data = []
        for condition in conditions:
            serializer = ConditionSerializer(condition, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "특정 날짜의 컨디션 기록이 수정되었습니다.", "data": response_data}, status=status.HTTP_200_OK)
    
    def delete(self, request, date):
        conditions = Condition.objects.filter(date=date)
        if not conditions.exists():
            return Response({"message": "해당 날짜에 대한 컨디션 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        conditions.delete()
        return Response({"message": "특정 날짜의 컨디션 기록이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)