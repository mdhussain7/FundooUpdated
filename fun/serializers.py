from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact


class UserContact(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
