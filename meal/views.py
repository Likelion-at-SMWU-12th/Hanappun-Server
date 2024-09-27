# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Ingredient, Meal
# from .serializers import IngredientSerializer, MealSerializer
# from datetime import datetime

# class MealListGETAPIView(APIView):
#     def get(self, username, request):
#         # 날짜가 쿼리 파라미터에 있는 경우 해당 날짜에 맞는 식사를 반환
#         date_str = request.query_params.get('date', None)
#         if date_str:
#             try:
#                 date = datetime.strptime(date_str, '%Y-%m-%d').date()
#                 meals = Meal.objects.filter(user=username, date=date)
#                 if not meals.exists():
#                     return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
#             except ValueError:
#                 return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             meals = Meal.objects.filter(user=username)

#         serializer = MealSerializer(meals, many=True)
#         return Response(serializer.data)


# class MealListCreateAPIView(APIView):
#     def post(self, request):
#         user_username = request.data.get('user')
#         user = get_object_or_404(User, username=user_username)  # 유저를 username으로 가져오기
#         data = request.data.copy()
#         data['user'] = user.id  # 유저 모델과 연결하여 ID 값을 설정

#         serializer = MealSerializer(data=data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "식사 기록이 생성되었습니다."}, status=status.HTTP_201_CREATED)
#         return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# class MealDetailByDateAPIView(APIView):
#     def put(self, username, request):
#         # 날짜를 쿼리 파라미터로 받아서 해당 날짜의 기록을 업데이트
#         date_str = request.query_params.get('date', None)
#         if date_str:
#             try:
#                 date = datetime.strptime(date_str, '%Y-%m-%d').date()
#                 meal = Meal.objects.filter(user=username, date=date).first()
#                 if not meal:
#                     return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
#             except ValueError:
#                 return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # 쿼리 파라미터로 받은 날짜를 validated_data에 추가
#         data = request.data.copy()
#         data['date'] = date_str  # 날짜 필드를 추가

#         serializer = MealSerializer(meal, data=data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, username, request):
#         # 날짜를 쿼리 파라미터로 받아서 해당 날짜의 기록을 삭제
#         date_str = request.query_params.get('date', None)
#         if date_str:
#             try:
#                 date = datetime.strptime(date_str, '%Y-%m-%d').date()
#                 meal = Meal.objects.filter(user=username, date=date).first()
#                 if not meal:
#                     return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
#             except ValueError:
#                 return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

#         meal.delete()
#         return Response({"message": "특정 날짜의 식사 기록이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# # Ingredient CRUD
# class IngredientListCreateAPIView(APIView):
#     def get(self, request):
#         ingredients = Ingredient.objects.all()
#         serializer = IngredientSerializer(ingredients, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = IngredientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class IngredientDetailAPIView(APIView):
#     def get(self, request, pk):
#         ingredient = get_object_or_404(Ingredient, pk=pk)
#         serializer = IngredientSerializer(ingredient)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         ingredient = get_object_or_404(Ingredient, pk=pk)
#         serializer = IngredientSerializer(ingredient, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         ingredient = get_object_or_404(Ingredient, pk=pk)
#         ingredient.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Meal, Ingredient
from .serializers import MealSerializer
from django.shortcuts import get_object_or_404
from users.models import User  # 사용자 모델 가져오기
from datetime import datetime

class MealListCreateAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                meals = Meal.objects.filter(user=user, date=date)
                if not meals.exists():
                    return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            meals = Meal.objects.filter(user=user)

        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = MealSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealDetailByDateAPIView(APIView):
    def get(self, request, username):
        # URL에서 전달된 사용자 이름을 기반으로 사용자를 조회
        user = get_object_or_404(User, username=username)

        # 날짜를 쿼리 파라미터로 받아서 해당 날짜의 기록을 조회
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                meals = Meal.objects.filter(user=user, date=date)
                if not meals.exists():
                    return Response({"error": f"No meals found for {date_str}."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Date parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # 해당 날짜와 사용자에 맞는 식사 기록 조회
                meal = Meal.objects.filter(user=user, date=date).first()
                if not meal:
                    return Response({"error": f"{date_str}에 해당하는 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "잘못된 날짜 형식입니다. YYYY-MM-DD 형식을 사용하세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "날짜 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    # request-body에서 'name'에 해당하는 메뉴를 업데이트
        menu_name = request.data.get('name', None)
        if menu_name:
            meal_item = Meal.objects.filter(user=user, date=date, name=menu_name).first()
            if not meal_item:
                return Response({"error": f"{menu_name} 메뉴를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 쿼리 파라미터로 받은 날짜를 request 데이터에 추가
            data = request.data.copy()
            data['date'] = date_str  # 날짜 필드를 추가

        # user를 context에 포함시켜서 serializer로 전달
            serializer = MealSerializer(meal_item, data=data, context={'user': user, 'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"error": "'name' 필드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)

    # 날짜를 쿼리 파라미터로 받아서 해당 날짜의 기록을 삭제
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # 해당 날짜의 식사 기록을 조회
                meal = Meal.objects.filter(user=user, date=date).first()
                if not meal:
                    return Response({"error": f"{date_str}에 해당하는 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error": "잘못된 날짜 형식입니다. YYYY-MM-DD 형식을 사용하세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "날짜 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    # request-body에서 'name'에 해당하는 메뉴 삭제 기능 추가
        menu_name = request.data.get('name', None)
        if menu_name:
            meal_item = Meal.objects.filter(user=user, date=date, name=menu_name).first()
            if not meal_item:
                return Response({"error": f"{menu_name} 메뉴를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        # 메뉴 삭제
            meal_item.delete()
            return Response({"message": f"{menu_name} 메뉴가 삭제되었습니다."}, status=status.HTTP_200_OK)
    
        return Response({"error": "'name' 필드가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
