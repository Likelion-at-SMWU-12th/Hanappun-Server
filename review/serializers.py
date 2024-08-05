from rest_framework.serializers import ModelSerializer

from .models import Review
from users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname'] 

# minseo : 리뷰 
class ReviewSerializer(ModelSerializer):
    reviewer_nickname = UserSerializer(source='reviewer', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'