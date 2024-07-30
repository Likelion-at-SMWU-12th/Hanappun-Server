from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# minseo : UserManager
class UserManager(BaseUserManager):
    # minseo : 기본 유저 생성
    def create_user(self, id, email, password, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수항목 입니다. ")

        user = self.model(
            id=id,
            email=email,  
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # minseo : 슈퍼 유저 생성
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# minseo : User 모델
class User(AbstractBaseUser):
    class Meta:
        db_table = "User"

    id = models.CharField("아이디", max_length=50, unique=True, primary_key=True)
    nickname = models.CharField("닉네임", max_length=15)
    email = models.EmailField("이메일", unique=True)
    friends = models.ManyToManyField("self", symmetrical=False, related_name='friends_set', blank=True)

    constitution_8_categories = (
        ('Hepatonia', '목양'),
        ('Cholecystonia', '목음'),
        ('Renotonia', '수양'),
        ('Vesicotonia', '수음'),
        ('Pulmotonia', '금양'),
        ('Colonotonia', '금음'),
        ('Pancreotonia', '토양'),
        ('Gastrotonia', '토음')
    )
    constitution_8 = models.CharField("8체질", choices=constitution_8_categories, max_length=50, blank=True)
    my_clinic = models.CharField("나의 한의원", max_length=15, blank=True)

    objects = UserManager()
