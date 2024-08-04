from django.db import models

from users.models import User
from clinic.models import Clinic

# Create your models here.

# minseo : 예약 모델
class Reservation(models.Model):
    client = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='환자 아이디')
    date = models.DateTimeField(verbose_name="예약일정")

    def to_json(self):
        return {
            "reservation_id": self.id,
            "client_username": self.client.username,
            "client_my_clinic":self.client.my_clinic.name,
            "date": self.date.isoformat(),
        }
