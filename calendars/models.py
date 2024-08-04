from django.db import models
from users.models import User
from condition.models import Condition

# minseo : 특정일의 이벤트(예약정보, 식습관, 컨디션)
class Event(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.JSONField()
