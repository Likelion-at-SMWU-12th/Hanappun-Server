from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Meal, Ingredient
from .serializers import IngredientSerializer, MealSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime

class MealListCreateAPIView(APIView):
    def get(self, request):
        # 날짜가 쿼리 파라미터에 있는 경우 해당 날짜에 맞는 식사를 반환
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()  # YYYY-MM-DD 형식으로 날짜 변환
                meals = Meal.objects.filter(user=request.user, date=date)
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

class MealDetailAPIView(APIView):
    def get(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk, user=request.user)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    def put(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk, user=request.user)
        serializer = MealSerializer(meal, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        meal = get_object_or_404(Meal, pk=pk, user=request.user)
        meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
