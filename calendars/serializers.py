from rest_framework import serializers
from .models import User, Appointment, EatingHabit, ConditionStatus

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'date', 'time', 'description']

class EatingHabitSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EatingHabit
        fields = ['id', 'user', 'date', 'total_evaluation']

class ConditionStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ConditionStatus
        fields = ['id', 'user', 'date', 'status']
