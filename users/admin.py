from django.contrib import admin
from .models import User

# Register your models here.

# minseo : admin에 모델 등록
@admin.register(User) 
class PostModelAdmin(admin.ModelAdmin):
    pass # 빈 클래스