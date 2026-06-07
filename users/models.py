from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="День рождения")

    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    bio = models.TextField(blank=True, verbose_name="О себе")