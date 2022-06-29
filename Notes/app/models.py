# coding=utf-8
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class CustomUser(models.Model):
    username = models.CharField(unique=True, max_length=15)
    date_of_birth = models.DateField(null=True)
    status = models.CharField(max_length=140, null=True)
    bio = models.TextField(null=True)
    password = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()

        return check_password(raw_password, self.password, setter)

    def is_authenticated(self):
        return True


class Note(models.Model):
    dt = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(CustomUser, related_name='user_notes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return self.title
