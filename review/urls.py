from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import ReviewViewSet, CountReviewCategory

app_name='review'

router = routers.DefaultRouter()
router.register(r'', ReviewViewSet)

urlpatterns=[
    path("", include(router.urls)),
    path('admin', admin.site.urls),
    path('cate/<int:clinic_id>/', CountReviewCategory.as_view(), name='clinic-review-category-count'),

]