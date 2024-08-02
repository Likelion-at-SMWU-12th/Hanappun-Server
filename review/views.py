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
    def get(self, request, clinic_id):
        review_counts = Review.objects.filter(clinic_id=clinic_id).values('review_cate').annotate(count=Count('review_cate'))
        response_data = {item['review_cate']: item['count'] for item in review_counts}

        return Response(response_data, status=status.HTTP_200_OK)