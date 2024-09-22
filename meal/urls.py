from django.urls import path
from .views import MealListCreateAPIView, MealDetailByDateAPIView,  IngredientListCreateAPIView, IngredientDetailAPIView


urlpatterns = [
    path('meal/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('meal/date/', MealDetailByDateAPIView.as_view(), name='meal-detail-by-date'),  # 날짜 기반 수정 및 삭제
    path('ingredients/', IngredientListCreateAPIView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailAPIView.as_view(), name='ingredient-detail'),
]
