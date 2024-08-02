from django.urls import path, include
from django.contrib import admin
from users import views
from rest_framework import routers
from .views import ClinicViewSet

app_name='clinic'

router = routers.DefaultRouter()
router.register(r'', ClinicViewSet)

urlpatterns=[
    path("", include(router.urls)),
    path('admin', admin.site.urls),
]