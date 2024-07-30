from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("friends", )
    
    # minseo : 회원가입
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    # minseo : 로그인
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nickname", "email", "friends", "constitution_8")

