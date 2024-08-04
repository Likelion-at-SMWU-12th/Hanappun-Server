from rest_framework import serializers
from .models import Event

from condition.models import Condition

# minseo : 컨디션 시리얼라이저
class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

# minseo : 식단 기록 시리얼라이저
# class MealSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = 
#         fields = '__all__'

# minseo : 이벤트 시리얼라이저
class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'