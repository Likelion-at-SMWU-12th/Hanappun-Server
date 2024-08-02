from django.contrib import admin
from .models import Clinic, ClinicImage

# Register your models here.

# minseo : admin에 모델 등록
@admin.register(Clinic) 
class PostModelAdmin(admin.ModelAdmin):
    pass # 빈 클래스

@admin.register(ClinicImage) 
class PostModelAdmin(admin.ModelAdmin):
    pass # 빈 클래스