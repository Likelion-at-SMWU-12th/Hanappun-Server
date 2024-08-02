from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Reservation
from users.models import User

# minseo : 예약자의 나의 한의원 정보를 갖고오기
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'my_clinic'] 

# minseo : 예약 
class ReservationSerializer(ModelSerializer):
    client = UserSerializer()  

    class Meta:
        model = Reservation
        fields = ['id', 'client', 'date']  

# minseo : 예약 시에 
class ReservationCreateSerializer(ModelSerializer):
    client = PrimaryKeyRelatedField(queryset=User.objects.all()) 

    class Meta:
        model = Reservation
        fields = ['id', 'client', 'date']