from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import BoardSerializer, UserSerializer, TaskSerializer
from .models import Board, Task, Category
from django.core import serializers
from django.http import HttpResponse
from datetime import datetime


# Create your views here.
class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
    def get_group(self, board_users_list):
        numberOfGroups = Group.objects.filter(name__contains='boardgroup').count()
        newGroup = Group.objects.get_or_create(name=f"boardgroup{numberOfGroups}")
        newGroup = newGroup[0]
        newGroup.user_set.set(board_users_list)
        return newGroup[0]
    
    def create(self, request, *args, **kwargs):
        board_users_raw = request.data.get('board_users', None)
        board_users_list = User.objects.filter(id__in=board_users_raw)
        boss_name = request.data.get("user_boss", None)
        user_boss = User.objects.filter(username=boss_name)
        board = Board.objects.create(
            name=request.data.get("name", None),
            user_boss=user_boss[0],
            group=self.get_group(self, board_users_list)
        )
        for user in board_users_list:
            board.board_users.add(user)
        serialzed_board = serializers.serialize('json',[board])
        return HttpResponse(serialzed_board, content_type='application/json')
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        boardname = self.kwargs.get('boardname', None)
        if boardname:
            board = Board.objects.get(name=boardname)
            print(board.name)
            queryset = self.queryset.filter(groups__name=board.group.name)
            return queryset
        return self.queryset
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_category(self, request):
        category_name = request.data.get("category", None)
        category_name = category_name['name']
        category = Category.objects.get(name=category_name)
        return category
    
    def get_board(self):
        board_name = self.kwargs.get('boardname', None)
        board = Board.objects.get(name=board_name)
        return board
    
    def get_group(self, assigned_usersList):
        numberOfGroups = Group.objects.filter(name__contains='taskGroup').count()
        newGroup = Group.objects.get_or_create(name=f"taskGroup{numberOfGroups}")
        newGroup = newGroup[0]
        newGroup.user_set.set(assigned_usersList)
        return newGroup
    
    def get_due_date(self, request):
        due_date = request.data.get("due_date", None)
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
        return due_date
    
    def get_queryset(self):
        boardname = self.kwargs.get('boardname', None)
        if boardname:
            queryset = self.queryset.filter(board__name=boardname)
            return queryset
        return self.queryset
    
    def create(self, request, **kwargs):
        assigned_usersRaw = request.data.get("assigned_users", [])
        assigned_usersList = User.objects.filter(id__in=assigned_usersRaw)
        task = Task.objects.create(priority= request.data.get("priority", None),
                                   title = request.data.get("title", None), 
                                   description= request.data.get("description", None),
                                   due_date=self.get_due_date(request),
                                   status=request.data.get("status", None),
                                   assigned_users_group=self.get_group(assigned_usersList),
                                   board=self.get_board(),
                                   category=self.get_category(request))
        for user in assigned_usersList:
            task.assigned_users.add(user)
        serialzed_task = serializers.serialize('json',[task])
        return HttpResponse(serialzed_task, content_type='application/json')
    
    