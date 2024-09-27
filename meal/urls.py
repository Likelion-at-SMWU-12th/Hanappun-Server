# from django.urls import path
# from .views import MealListGETAPIView, MealListCreateAPIView, IngredientDetailAPIView, MealDetailByDateAPIView,  IngredientListCreateAPIView, IngredientDetailAPIView


# urlpatterns = [
#     path('meal/', MealListCreateAPIView.as_view(), name='meal-list-create'),
#     path('meal/<str:username>', MealListGETAPIView.as_view(), name='meal-list-get'),
#     path('meal/<str:username>/date', MealDetailByDateAPIView.as_view(), name='meal-detail-by-date'),  # 날짜 기반 수정 및 삭제
#     path('ingredients/', IngredientListCreateAPIView.as_view(), name='ingredient-list-create'),
#     path('ingredients/<int:pk>/', IngredientDetailAPIView.as_view(), name='ingredient-detail'),
# ]

from django.urls import path
from .views import MealListCreateAPIView, MealDetailByDateAPIView, DeleteMealDetailByDateAPIView, GetMealDataByID

urlpatterns = [
    path('meal/<str:username>/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('meal/<str:username>/date/', MealDetailByDateAPIView.as_view(), name='meal-detail-by-date'),  # 날짜 기반 수정 및 삭제
    path('meal/<str:username>/<int:foodID>', DeleteMealDetailByDateAPIView.as_view(), name='meal-delete-by-name'),
    path('meal/<str:username>/<int:id>', GetMealDataByID.as_view(), name='meal-list-create'),
]
