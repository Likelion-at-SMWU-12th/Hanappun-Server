from django.contrib import admin
from .models import Reservation
# Register your models here.

# minseo : admin에 모델 등록
@admin.register(Reservation) 
class PostModelAdmin(admin.ModelAdmin):
    pass # 빈 클래스