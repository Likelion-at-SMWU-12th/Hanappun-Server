from django.shortcuts import render
from django.http import JsonResponse
from .models import Appointment, EatingHabit, ConditionStatus, User

def get_calendar_events(request):
    date = request.GET.get('date')

    appointments = Appointment.objects.filter(date=date).select_related('user')
    eating_habits = EatingHabit.objects.filter(date=date).select_related('user')
    condition_statuses = ConditionStatus.objects.filter(date=date).select_related('user')

    response = {
        "appointments": [
            {
                "user": appointment.user.name,
                "date": appointment.date,
                "time": appointment.time,
                "description": appointment.description
            }
            for appointment in appointments
        ],
        "eating_habits": [
            {
                "user": eating_habit.user.name,
                "total_evaluation": eating_habit.total_evaluation
            }
            for eating_habit in eating_habits
        ],
        "condition_statuses": [
            {
                "user": condition_status.user.name,
                "status": condition_status.status
            }
            for condition_status in condition_statuses
        ],
    }

    return JsonResponse(response)
