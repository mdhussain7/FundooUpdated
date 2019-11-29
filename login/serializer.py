from rest_framework import serializers
from django.contrib.auth.models import User


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class ForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class LogoutSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
