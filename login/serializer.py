from rest_framework import serializers
from .models import UserProfile
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


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='id')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'image', 'user', 's3_image_link']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'image', 'user']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'image']
