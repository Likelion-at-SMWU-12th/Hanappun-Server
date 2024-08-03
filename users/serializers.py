from rest_framework.serializers import ModelSerializer, CharField, ValidationError, Serializer
from django.contrib.auth import get_user_model
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
    
# minseo : 프로필 조회, 수정에 사용
class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "nickname", "email", "friends", "constitution_8", "my_clinic")

# minseo : 우리 케어 친구 신청
class AcceptFriendRequestSerializer(Serializer):
    my_username = CharField()
    friend_username = CharField()

    def validate_friend_username(self, value):
        User = get_user_model()
        if not User.objects.filter(username=value).exists():
            raise ValidationError("사용자가 존재하지 않습니다.")
        return value

    def validate(self, data):
        my_username = data['my_username']
        friend_username = data['friend_username']
        User = get_user_model()
        try:
            my = User.objects.get(username=my_username)
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            raise ValidationError("사용자가 존재하지 않습니다.")
        
        if friend == my:
            raise ValidationError("자신에게는 우리 케어 신청을 할 수 없습니다.")
        
        if friend in my.friends.all():
            raise ValidationError("이미 우리 케어 관계입니다.")
        
        return data

# minseo : 모든 친구 리스트 보기 
class FriendsListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("friends", )

# minseo : 친구 삭제
class DeleteFriendSerializer(Serializer):
    friend_username = CharField()

    def validate_friend_username(self, value):
        User = get_user_model()
        if not User.objects.filter(username=value).exists():
            raise ValidationError("사용자가 존재하지 않습니다.")
        return value