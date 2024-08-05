from django.urls import path
from .views import MealAPIView

urlpatterns = [
    path('meal/', MealAPIView.as_view(), name='meal_list_create_update_delete'),  # GET, POST, PUT, DELETE
    path('meal/<str:date>/', MealAPIView.as_view(), name='meal_by_date'),  # GET
]