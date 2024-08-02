from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import ReservationViewSet, ReservationByDateView

app_name='reservation'

router = routers.DefaultRouter()
router.register(r'', ReservationViewSet)

urlpatterns=[
    path("", include(router.urls)),
    path('admin', admin.site.urls),
    path('date/<str:date>/', ReservationByDateView.as_view(), name='reservations-by-date'),

]