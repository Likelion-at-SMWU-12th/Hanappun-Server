# urls.py
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ConditionCreateView, ConditionListView, ConditionUpdateView, ConditionDeleteView, ConditionByDateView

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('condition/', ConditionCreateView.as_view(), name='condition-create'),
    path('conditions/', ConditionListView.as_view(), name='condition-list'),
    #path('condition/<int:pk>/', ConditionUpdateView.as_view(), name='condition-update'),
    #path('condition/delete/<int:pk>/', ConditionDeleteView.as_view(), name='condition-delete'),
    path('condition/<str:date>/', ConditionByDateView.as_view(), name='condition-by-date'),
]
