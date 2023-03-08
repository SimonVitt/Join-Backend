from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import CreateUserauthSerializer, LoginSerializer
from knox import views as knox_views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

class CreateUserApi(CreateAPIView):
    http_method_names = ['post']

    serializer_class = CreateUserauthSerializer
    permission_classes = [AllowAny,]

class LoginAPIView(knox_views.LoginView):
    http_method_names = ['post']

    serializer_class = LoginSerializer
    permission_classes = [AllowAny,]
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return JsonResponse({'errors':serializer.errors})
        return Response(response.data)
        
    
''''
class UserLogIn(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        token = Token.objects.get(user=user)
        return JsonResponse({
            'token': token.key,
            'id': user.pk,
            'username': user.username
        })
        '''