from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
from datetime import date


# Create your models here.
class Board(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='boardUser', null=True)
    board_users = models.ManyToManyField(User)
    name = models.CharField(max_length=500)
    user_boss = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boardBoss')

class Category(models.Model):
    name = models.CharField(max_length=500)
    color = models.CharField(max_length=500)

class Task(models.Model):
    priority = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    status = models.CharField(max_length=500)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    assigned_users_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    assigned_users = models.ManyToManyField(User)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)