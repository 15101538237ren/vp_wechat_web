from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    phone_num = models.CharField(null=False, unique=True, max_length=20)