from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    phone_num = models.CharField(null=False, unique=False, max_length=20)
    step=models.IntegerField(null=True,default=1)