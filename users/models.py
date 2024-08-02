from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from clinic.models import Clinic

# minseo : UserManager
class UserManager(DjangoUserManager):
    # minseo : 기본 유저 생성
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수항목 입니다. ")

        user = self.model(
            username=username,
            email=email,  
            password=password,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return super().create_superuser(username, email, password, **extra_fields) # 수퍼 클래스의 create_superuser 호출
    

# minseo : User 모델
class User(AbstractUser):
    class Meta:
        db_table = "User"

    username = models.CharField("아이디", max_length=50, unique=True, primary_key=True)
    nickname = models.CharField("닉네임", max_length=15)
    email = models.EmailField("이메일", unique=True, blank=True)
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
    my_clinic = models.ForeignKey(Clinic, verbose_name="나의 한의원", on_delete=models.SET_NULL, blank=True, null=True)

    objects = UserManager()

