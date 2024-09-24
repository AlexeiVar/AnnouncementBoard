from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# Причина создания кастомного юзера проста, это позволит в случае необходимости добавить функционал к юзеру
class CustomUser(AbstractUser):
    pass


# Категории
class Categories(models.Model):
    name = models.CharField(max_length=25)
    subscribers = models.ManyToManyField(CustomUser, blank=True, related_name='categories')
    
    def __str__(self):
        return self.name


# Объявления
class Announcement(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Отклики на объявления
class Response(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField()
    acceptance = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.acceptance = True
        self.save()
