from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Board, Task, Category

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
    
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields= ['name', 'color']
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    assigned_users_group = GroupSerializer()
    assigned_users = UserSerializer(many=True)
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'category', 'assigned_users_group', 'assigned_users']

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    board_users = UserSerializer(many=True)
    user_boss = UserSerializer()
    group = GroupSerializer()
    class Meta:
        model = Board
        fields = ['name', 'group', 'user_boss', 'board_users']
