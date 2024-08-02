from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .serializers import ReviewSerializer
from .models import Review

# Create your views here.

# minseo : 리뷰 CRUD 뷰셋
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # 한의원 별 리뷰 조회하기
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['clinic']

# minseo : 특정 한의원의 리뷰 카테고리 합계
class CountReviewCategory(APIView):
    def get(self, request, clinic_id, format=None):
        reviews = Review.objects.filter(clinic_id=clinic_id)

        count_facility = reviews.filter(is_selected_Facility=True).count()
        count_prescription = reviews.filter(is_selected_Prescription=True).count()
        count_health = reviews.filter(is_selected_Health=True).count()
        count_kindness = reviews.filter(is_selected_Kindness=True).count()

        data = {
            'facility_count': count_facility,
            'prescription_count': count_prescription,
            'health_count': count_health,
            'kindness_count': count_kindness,
        }

        return Response(data, status=status.HTTP_200_OK)