# from django.db import models
# # from users.models import User

# class BodyType(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class AnimalProtein(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class VegetableProtein(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Carbohydrate(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class RootVegetables(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Vegetables(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Herb(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Seaweed(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Fruit(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Ingredient(models.Model):
#     name = models.CharField(max_length=100)
#     score = models.IntegerField()

#     def __str__(self):
#         return self.name

# class Meal(models.Model):
#     TIMING_CHOICES = [
#         ('morning', '아침'),
#         ('lunch', '점심'),
#         ('dinner', '저녁'),
#         ('snack', '간식'),
#     ]
    
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100, verbose_name='식사명')
#     date = models.DateField(verbose_name='식사날짜')
#     timing = models.CharField(max_length=10, choices=TIMING_CHOICES, verbose_name='식사시간')
#     ingredients = models.ManyToManyField(Ingredient, related_name='meals', verbose_name='성분')
#     total = models.IntegerField(verbose_name='총점', default=0)

#     def __str__(self):
#         return f'{self.name} ({self.date})'
    
#     from django.db import models

from django.db import models
from users.models import User  # users 앱에서 User 모델을 가져옵니다.

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meal(models.Model):
    TIMING_CHOICES = [
        ('morning', '아침'),
        ('lunch', '점심'),
        ('dinner', '저녁'),
        ('snack', '간식'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='식사명')
    date = models.DateField(verbose_name='식사날짜')
    timing = models.CharField(max_length=10, choices=TIMING_CHOICES, verbose_name='식사시간')
    ingredients = models.ManyToManyField(Ingredient, related_name='meals', verbose_name='성분')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')  # 사용자 정보 저장
    total = models.IntegerField(verbose_name='총점', default=0)

    def __str__(self):
        return f'{self.name} ({self.date})'
