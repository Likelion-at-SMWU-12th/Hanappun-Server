from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.models import User
from .models import Meal, Menu, AnimalProtein, VegetableProtein, Carbohydrate, RootVegetables, Vegetables, Herb, Seaweed, Fruit
from .serializers import MealSerializer, MenuSerializer

# 체질별 맞는 요소와 맞지 않는 요소 정의
body_type_preferences = {
    '목양': {
        'likes': ['민물생선', '오리고기', '닭고기', '토마토', '우유', '소고기', '밀가루', '고구마', '감자', '마늘'],
        'dislikes': ['바다생선', '조개류', '갑각류', '청포도', '팥', '복분자', '보리', '메밀', '오이', '모과', '돼지고기', '시금치', '고추', '딸기', '미역']
    },
    '목음': {
        'likes': ['치즈', '콩', '백미', '가지', '옥수수', '쇠고기', '돼지고기', '밀가루', '감자', '마늘'],
        'dislikes': ['바다생선', '조개류', '청포도', '와인', '찹쌀', '생강', '오이', '복분자', '꿀', '닭고기', '현미', '보리', '고구마', '토마토']
    },
    '토양': {
        'likes': ['아보카도', '갑각류', '우유', '백미', '콩', '돼지고기', '소고기', '복어'],
        'dislikes': ['도라지', '현미', '미역', '망고', '고추', '참기름', '고구마', '토마토', '녹용', '밤', '옥수수', '시금치', '감자', '사과', '김']
    },
    '토음': {
        'likes': ['딸기', '치즈', '조개류', '팥', '견과류', '돼지고기', '복어'],
        'dislikes': ['닭고기', '오리고기', '밤', '현미', '도라지', '마늘', '토마토', '고구마', '도토리', '마', '콩', '쇠고기', '감자', '가지', '김']
    },
    '금양': {
        'likes': ['굴', '갑각류', '두부', '오이', '애호박', '바다생선', '조개류', '백미', '배추', '상추'],
        'dislikes': ['쇠고기', '닭고기', '유제품', '콩', '밀가루', '돼지고기', '치즈', '현미', '고구마', '호박', '미역', '토마토', '수박', '팥', '보리']
    },
    '금음': {
        'likes': ['갑각류', '복어', '된장', '두부', '오이', '바다생선', '흰살생선', '백미', '배추', '상추'],
        'dislikes': ['쇠고기', '바다생선', '백미', '배추', '조개류', '치즈', '현미', '고구마', '도라지', '호박', '굴', '팥', '보리', '옥수수', '깻잎']
    },
    '수양': {
        'likes': ['흰살생선', '콩', '밤', '백미', '고구마', '감자', '닭고기', '오리고기', '사과'],
        'dislikes': ['돼지고기', '복어', '팥', '보리', '알로에', '감', '참외', '붉은살생선', '조개류', '쇠고기', '유제품', '바다생선', '민물생선', '청국장']
    },
    '수음': {
        'likes': ['민물생선', '버터', '콩', '밤', '백미', '된장', '쇠고기', '닭고기', '감자', '사과'],
        'dislikes': ['청포도', '팥', '복어', '갑각류', '돼지고기', '바다생선', '조개류', '흰살생선', '메밀', '오이', '시금치', '두유', '배추', '상추', '김']
    }
}

# 체질별 구성요소 점수 정의
component_scores = {
    '목양': {
        '50': ['민물생선', '오리고기', '닭고기', '토마토', '우유'],
        '30': ['소고기', '밀가루', '고구마', '감자', '마늘'],
        '-10': ['돼지고기', '시금치', '고추', '딸기', '미역'],
        '-30': ['복분자', '보리', '메밀', '오이', '모과'],
        '-50': ['바다생선', '조개류', '갑각류', '청포도', '팥']
    },
    '목음': {
        '50': ['치즈', '콩', '백미', '가지', '옥수수'],
        '30': ['쇠고기', '돼지고기', '밀가루', '감자', '마늘'],
        '-10': ['닭고기', '현미', '보리', '고구마', '토마토'],
        '-30': ['찹쌀', '생강', '오이', '복분자', '꿀'],
        '-50': ['바다생선', '조개류', '청포도', '와인']
    },
    '토양': {
        '50': ['돼지고기', '소고기', '복어'],
        '30': ['아보카도', '갑각류', '우유', '백미', '콩'],
        '-10': ['옥수수', '시금치', '감자', '사과', '김'],
        '-30': ['참기름', '고구마', '토마토', '녹용', '밤'],
        '-50': ['도라지', '현미', '미역', '망고', '고추']
    },
    '토음': {
        '50': ['돼지고기', '복어'],
        '30': ['딸기', '치즈', '조개류', '팥', '견과류'],
        '-10': ['콩', '쇠고기', '감자', '가지', '김'],
        '-30': ['마늘', '토마토', '고구마', '도토리', '마'],
        '-50': ['닭고기', '오리고기', '밤', '현미', '도라지']
    },
    '금양': {
        '50': ['바다생선', '조개류', '백미', '배추', '상추'],
        '30': ['굴', '갑각류', '두부', '오이', '애호박'],
        '-10': ['미역', '토마토', '수박', '팥', '보리'],
        '-30': ['돼지고기', '치즈', '현미', '고구마', '호박'],
        '-50': ['쇠고기', '닭고기', '유제품', '콩', '밀가루']
    },
    '금음': {
        '50': ['바다생선', '흰살생선', '백미', '배추', '상추'],
        '30': ['갑각류', '복어', '된장', '두부', '오이'],
        '-10': ['굴', '팥', '보리', '옥수수', '깻잎'],
        '-30': ['치즈', '현미', '고구마', '도라지', '호박'],
        '-50': ['쇠고기', '바다생선', '백미', '배추', '조개류']
    },
    '수양': {
        '50': ['감자', '닭고기', '오리고기', '사과'],
        '30': ['흰살생선', '콩', '밤', '백미', '고구마'],
        '-10': ['쇠고기', '유제품', '바다생선', '민물생선', '청국장'],
        '-30': ['감', '참외', '붉은살 생선', '조개류'],
        '-50': ['돼지고기', '복어', '팥', '보리', '알로에']
    },
    '수음': {
        '50': ['된장', '쇠고기', '닭고기', '감자', '사과'],
        '30': ['민물생선', '버터', '콩', '밤', '백미'],
        '-10': ['시금치', '두유', '배추', '상추', '김'],
        '-30': ['바다생선', '조개류', '흰살생선', '메밀', '오이'],
        '-50': ['청포도', '팥', '복어', '갑각류', '돼지고기']
    }
}

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

# 체질에 따른 구성요소 점수 계산
def calculate_score(body_type, components):
    score = 0
    scores = component_scores[body_type]
    for component in components:
        for score_value, items in scores.items():
            if component in items:
                score += int(score_value)
                break
    return score

class MealAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response({"message": "식사 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)

        # if date:
        #     meals = Meal.objects.filter(date=date)
        #     if not meals.exists():
        #         return Response({"message": "해당 날짜에 대한 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        #     serializer = MealSerializer(meals, many=True)
        #     return Response({"message": "특정 날짜의 식사 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)
        # else:
        #     meals = Meal.objects.all()
        #     serializer = MealSerializer(meals, many=True)
        #     return Response({"message": "식사 기록 조회 성공", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        user_username = request.data.get('username')
        # constitution_8 = request.data.get('constitution_8')
        date = request.data.get('date')
        
        if not user_username or not date:
            return Response({"message": "username, date는 필수 항목입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(username=user_username)
        except User.DoesNotExist:
            return Response({"message": "사용자가 존재하지 않습니다.",}, status = status.HTTP_404_NOT_FOUND)
        
        # user.save()
        
        data = request.data.copy()
        data['user'] = user
    
        meal = Meal.objects.create(user=user, date=data['date'])
        
        total_score = 0
        classified_meals = {
            'morning': {'좋은 음식': [], '나쁜 음식': []},
            'lunch': {'좋은 음식': [], '나쁜 음식': []},
            'dinner': {'좋은 음식': [], '나쁜 음식': []},
            'snack': {'좋은 음식': [], '나쁜 음식': []}
        }

        response_data = {
            "username": user.username,
            "constitution_8": user.constitution_8,
            "date": meal.date,
            "morning": [],
            "lunch": [],
            "dinner": [],
            "snack": []
        }

        for meal_time in ['morning', 'lunch', 'dinner', 'snack']:
            if meal_time in data:
                menus = []
                for menu_data in data[meal_time]:
                    menu = create_menu(menu_data)
                    menus.append(menu)
                    serialized_menu = MenuSerializer(menu).data
                    response_data[meal_time].append(serialized_menu)
                getattr(meal, meal_time).set(menus)

                # 체질에 따른 음식 점수 계산 및 분류
                for menu_data in data[meal_time]:
                    components = menu_data.get('animal_protein', []) + menu_data.get('vegetable_protein', []) + menu_data.get('carbohydrate', []) + menu_data.get('root_vegetables', []) + menu_data.get('vegetables', []) + menu_data.get('herb', []) + menu_data.get('seaweed', []) + menu_data.get('fruit', [])
                    score = calculate_score(user.constitution_8, components)
                    total_score += score
                    if score >= 0:
                        classified_meals[meal_time]['좋은 음식'].append(menu_data['menu_name'])
                    else:
                        classified_meals[meal_time]['나쁜 음식'].append(menu_data['menu_name'])

        meal.save()

        # 전체 점수에 따른 상태 분류
        if total_score < 0:
            overall_status = "bad"
        elif 0 <= total_score < 200:
            overall_status = "soso"
        else:
            overall_status = "good"

        response_data.update(classified_meals)
        response_data['overall_status'] = overall_status

        return Response({"message": "식사 기록이 생성되었습니다.", "data": response_data}, status=status.HTTP_201_CREATED)

    def put(self, request):
        date = request.data.get('date')
        meals = Meal.objects.filter(date=date)
        if not meals.exists():
            return Response({"message": "해당 날짜에 대한 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        user_username = request.data.get('username')
        user = get_object_or_404(User, username=user_username)
        
        constitution_8 = user.constitution_8

        data = request.data.copy()
        data['user'] = user

        for meal in meals:
            meal.user = user
            meal.save()

        total_score = 0
        classified_meals = {
            'morning': {'좋은 음식': [], '나쁜 음식': []},
            'lunch': {'좋은 음식': [], '나쁜 음식': []},
            'dinner': {'좋은 음식': [], '나쁜 음식': []},
            'snack': {'좋은 음식': [], '나쁜 음식': []}
        }

        response_data = {
            "username": user.username,
            "constitution_8": user.constitution_8,
            "date": date,
            "morning": [],
            "lunch": [],
            "dinner": [],
            "snack": []
        }

        for meal in meals:
            for meal_time in ['morning', 'lunch', 'dinner', 'snack']:
                if meal_time in data:
                    menus = []
                    for menu_data in data[meal_time]:
                        menu = create_menu(menu_data)
                        menus.append(menu)
                        serialized_menu = MenuSerializer(menu).data
                        response_data[meal_time].append(serialized_menu)
                    getattr(meal, meal_time).set(menus)

                    # 체질에 따른 음식 점수 계산 및 분류
                    for menu_data in data[meal_time]:
                        components = menu_data.get('animal_protein', []) + menu_data.get('vegetable_protein', []) + menu_data.get('carbohydrate', []) + menu_data.get('root_vegetables', []) + menu_data.get('vegetables', []) + menu_data.get('herb', []) + menu_data.get('seaweed', []) + menu_data.get('fruit', [])
                        score = calculate_score(constitution_8, components)
                        total_score += score
                        if score >= 0:
                            classified_meals[meal_time]['좋은 음식'].append(menu_data['menu_name'])
                        else:
                            classified_meals[meal_time]['나쁜 음식'].append(menu_data['menu_name'])

            meal.save()

        # 전체 점수에 따른 상태 분류
        if total_score < 0:
            overall_status = "bad"
        elif 0 <= total_score < 200:
            overall_status = "soso"
        else:
            overall_status = "good"
        response_data.update(classified_meals)
        response_data['overall_status'] = overall_status

        return Response({"message": "특정 날짜의 식사 기록이 수정되었습니다.", "data": response_data}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        date = request.data.get('date')
        meals = Meal.objects.filter(date=date)
        if not meals.exists():
            return Response({"message": "해당 날짜에 대한 식사 기록이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        meals.delete()
        return Response({"message": "특정 날짜의 식사 기록이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
