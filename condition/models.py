from django.db import models
#from django.conf import settings
# from django.contrib.auth.models import User
from users.models import User




class Condition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    condition_cate = models.CharField(max_length=255)
    mood_cate = models.CharField(max_length=255)
    memo = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
