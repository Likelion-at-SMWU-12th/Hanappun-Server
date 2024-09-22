from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ingredient, Meal
from .serializers import IngredientSerializer, MealSerializer
from datetime import datetime

class MealListCreateAPIView(APIView):
    def get(self, request):
        # 날짜가 쿼리 파라미터에 있는 경우 해당 날짜에 맞는 식사를 반환
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                meals = Meal.objects.filter(user=request.user, date=date)
                if not meals.exists():
                    return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            meals = Meal.objects.filter(user=request.user)

        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MealSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MealDetailByDateAPIView(APIView):
    def put(self, request):
        # 날짜를 쿼리 파라미터로 받아서 해당 날짜의 기록을 업데이트
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                meal = Meal.objects.filter(user=request.user, date=date).first()
                if not meal:
                    return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 쿼리 파라미터로 받은 날짜를 validated_data에 추가
        data = request.data.copy()
        data['date'] = date_str  # 날짜 필드를 추가

        serializer = MealSerializer(meal, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # 날짜를 쿼리 파라미터로 받아서 해당 날짜의 기록을 삭제
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                meal = Meal.objects.filter(user=request.user, date=date).first()
                if not meal:
                    return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        meal.delete()
        return Response({"message": "특정 날짜의 식사 기록이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# Ingredient CRUD
class IngredientListCreateAPIView(APIView):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetailAPIView(APIView):
    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
