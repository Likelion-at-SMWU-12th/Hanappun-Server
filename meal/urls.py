from django.urls import path
from .views import MealListCreateAPIView, MealDetailAPIView, IngredientListCreateAPIView, IngredientDetailAPIView

urlpatterns = [
    path('meal/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('meal/<int:pk>/', MealDetailAPIView.as_view(), name='meal-detail'),
    path('ingredients/', IngredientListCreateAPIView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailAPIView.as_view(), name='ingredient-detail'),
]
