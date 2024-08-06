from django.urls import path
from .views import MealAPIView, ViewMealByDate

urlpatterns = [
    path('meal/', MealAPIView.as_view(), name='meal_list_create_update_delete'),  # GET, POST, PUT, DELETE
    path('date/meal/<str:date>/', ViewMealByDate.as_view(), name='meal_by_date'),  # GET
]