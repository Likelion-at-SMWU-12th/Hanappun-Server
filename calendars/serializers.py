from rest_framework import serializers
from .models import Event

from condition.models import Condition
from users.models import User
from meal.models import Meal

# minseo : 컨디션 시리얼라이저
class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

# minseo : 식단 기록 시리얼라이저
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

# minseo : 이벤트 시리얼라이저
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['date', 'user', 'appointment']  

# minseo : 오늘의 이벤트
class TodayEventSerializer(serializers.ModelSerializer):
    pass

# minseo : 프로필 조회, 수정에 사용
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "friends", "constitution_8", "my_clinic")