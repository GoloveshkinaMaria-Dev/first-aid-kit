from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import MAX_NAME_LENGTH


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH, blank=False, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH, blank=False, verbose_name="Фамилия"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
