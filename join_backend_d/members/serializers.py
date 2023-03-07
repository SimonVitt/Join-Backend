from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
class CreateUserauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'required': True},
            'email': {'required': True}
        }
        
    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        username = attrs.get('username', '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email exists')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User exists')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if User.objects.filter(username=username).exists():
            user=authenticate(request=self.context.get('request'), username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Wrong credentials')
            attrs['user']=user
        else:
            raise serializers.ValidationError('Username doesnt exists')
        return attrs
        
    
    