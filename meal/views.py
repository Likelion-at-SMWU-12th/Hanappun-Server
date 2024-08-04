from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .models import Meal, Menu, AnimalProtein, VegetableProtein, Carbohydrate, RootVegetables, Vegetables, Herb, Seaweed, Fruit
from .serializers import MealSerializer, MenuSerializer
from users.models import User

# 헬퍼 함수: 구성 요소 이름을 ID로 변환
def get_ids_from_names(model, names):
    ids = []
    for name in names:
        objs = model.objects.filter(name=name)
        if objs.exists():
            ids.append(objs.first().id)
    return ids

def create_menu(data):
    menu = Menu.objects.create(menu_name=data['menu_name'])
    menu.animal_protein.set(get_ids_from_names(AnimalProtein, data.get('animal_protein', [])))
    menu.vegetable_protein.set(get_ids_from_names(VegetableProtein, data.get('vegetable_protein', [])))
    menu.carbohydrate.set(get_ids_from_names(Carbohydrate, data.get('carbohydrate', [])))
    menu.root_vegetables.set(get_ids_from_names(RootVegetables, data.get('root_vegetables', [])))
    menu.vegetables.set(get_ids_from_names(Vegetables, data.get('vegetables', [])))
    menu.herb.set(get_ids_from_names(Herb, data.get('herb', [])))
    menu.seaweed.set(get_ids_from_names(Seaweed, data.get('seaweed', [])))
    menu.fruit.set(get_ids_from_names(Fruit, data.get('fruit', [])))
    return menu

# Meal 기록 생성 뷰
class MealAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, date=None):
        if date:
            meals = Meal.objects.filter(date=date)
            if not meals.exists():
                return Response({"message": "해당 날짜에 대한 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            serializer = MealSerializer(meals, many=True)
            return Response({"message": "특정 날짜의 식사 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            meals = Meal.objects.all()
            serializer = MealSerializer(meals, many=True)
            return Response({"message": "식사 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        user_username = request.data.get('user')
        user = get_object_or_404(User, username=user_username)
        data = request.data.copy()
        data['user'] = user
        
        meal = Meal.objects.create(user=user, date=data['date'])
        
        for meal_time in ['morning', 'lunch', 'dinner', 'snack']:
            if meal_time in data:
                menus = []
                for menu_data in data[meal_time]:
                    menu = create_menu(menu_data)
                    menus.append(menu)
                getattr(meal, meal_time).set(menus)

        meal.save()
        serializer = MealSerializer(meal)
        return Response({"message": "식사 기록이 생성되었습니다.", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request):
        date = request.data.get('date')
        meals = Meal.objects.filter(date=date)
        if not meals.exists():
            return Response({"message": "해당 날짜에 대한 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        user_username = request.data.get('user')
        user = get_object_or_404(User, username=user_username)
        data = request.data.copy()
        data['user'] = user

        for meal in meals:
            for meal_time in ['morning', 'lunch', 'dinner', 'snack']:
                if meal_time in data:
                    menus = []
                    for menu_data in data[meal_time]:
                        menu = create_menu(menu_data)
                        menus.append(menu)
                    getattr(meal, meal_time).set(menus)
            meal.save()

        serializer = MealSerializer(meals, many=True)
        return Response({"message": "특정 날짜의 식사 기록이 수정되었습니다.", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        date = request.data.get('date')
        meals = Meal.objects.filter(date=date)
        if not meals.exists():
            return Response({"message": "해당 날짜에 대한 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        meals.delete()
        return Response({"message": "특정 날짜의 식사 기록이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
