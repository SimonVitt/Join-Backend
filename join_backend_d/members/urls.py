from django.urls import include, path
from . import views

urlpatterns = [
    path('create/', views.CreateUserApi.as_view()),
    path('login/', views.LoginAPIView.as_view())
]
