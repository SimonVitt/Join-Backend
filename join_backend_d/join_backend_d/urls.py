"""join_backend_d URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from board.views import BoardViewSet, UserViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r'boards/(?P<id>[\w-]+)', BoardViewSet)
router.register(r'alluser', UserViewSet, basename='AllUsers')
router.register(r'(?P<boardname>[\w-]+)/tasks', TaskViewSet, basename='allTasksBoard')
router.register(r'(?P<boardname>[\w-]+)/users', UserViewSet, basename='allUsersBoard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls'))
]
