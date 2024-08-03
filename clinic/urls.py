from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import ClinicViewSet, DoctorViewSet

app_name='clinic'

clinic_router = routers.DefaultRouter()
clinic_router.register(r'', ClinicViewSet)

doctor_router = routers.DefaultRouter()
doctor_router.register(r'', DoctorViewSet)


urlpatterns=[
    path("info/", include(clinic_router.urls)),
    path("doctor/", include(doctor_router.urls)),
    path('admin', admin.site.urls),
]