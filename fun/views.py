# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render
from rest_framework_swagger.views import get_swagger_view
from .serializers import ContactDataSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from rest_framework import status, generics

# Create your views here.
User = get_user_model()

schema_view = get_swagger_view(title='My FunDoo Application ')


def home(request):
    return render(request, 'fun/home.html')


class ContactData(generics.GenericAPIView):
    serializer_class = ContactDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        contact = Contact.objects.all()
        serializer = ContactDataSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)