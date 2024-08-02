from django.db import models
from users.models import User
from clinic.models import Clinic

# Create your models here.

# minseo : 리뷰 모델
class Review(models.Model):
    reviewer = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='작성자')
    content = models.TextField(verbose_name='리뷰 내용')
    clinic = models.ForeignKey(to=Clinic, on_delete=models.CASCADE, verbose_name='한의원')
    rate = models.IntegerField(verbose_name='별점')

    CATEGORY_CHOICES = [
        'Facility',
        'Prescription',
        'Health',
        'Kindness',
    ]

    is_selected_Facility = models.BooleanField(verbose_name='시설이 쾌적해요')
    is_selected_Prescription = models.BooleanField(verbose_name='약 처방이 잘 맞아요')
    is_selected_Health = models.BooleanField(verbose_name='건강 관리에 철저해요')
    is_selected_Kindness = models.BooleanField(verbose_name='의료진, 직원이 친절해요')
    
