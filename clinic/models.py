from django.db import models

# Create your models here.

# minseo : 한의원 모델
class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("한의원명", max_length=50)
    detail = models.TextField("한의원 설명")
    location = models.CharField("도로명주소", max_length=50)
    lat = models.FloatField("위도")
    lon = models.FloatField("경도")
    call = models.CharField("전화번호", max_length=50)
    
    clinic_categories = (
        ('HealthCare', '건강 관리'),
        ('Constitution_8', '8체질'),
        ('Herbal_prescription', '한약 처방'),
        ('Sasang_constitution', '사상체질'),
        ('Accident', '교통사고 전문'),
        ('Acupuncture', '침 치료'),
    )
    clinic_cate = models.CharField("한의원 카테고리", choices=clinic_categories, max_length=50, blank=True)
    

# minseo : 이미지 경로 지정 함수
def image_upload_path(instance, filename):
    return f'{instance.clinic.id}/{filename}'

# minseo : 한의원 다중 이미지 정보 모델
class ClinicImage(models.Model):
    id = models.AutoField(primary_key=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path)
