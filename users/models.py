from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Django User classi juda katta dastur bo'lib uni overwrite qilishda dastur yangi ishga tushganda Malumotlar bazamizda 
    malumotlar saqlamasdan yozib olishimiz kerak iloji bo'lsa """
    profile_picture = models.ImageField(default='default_user.png')
