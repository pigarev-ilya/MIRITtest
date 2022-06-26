# coding=utf-8
from django.db import models


# Create your models here.

class CustomUser(models.Model):
    name = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=140)
    bio = models.TextField()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class Note(models.Model):
    dt = models.DateTimeField()
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(CustomUser, related_name='user_notes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return self.title
