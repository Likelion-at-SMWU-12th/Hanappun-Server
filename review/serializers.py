from rest_framework.serializers import ModelSerializer

from .models import Review

# minseo : 리뷰 
class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'