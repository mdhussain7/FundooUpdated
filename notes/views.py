# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.shortcuts import render
#
# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Contacts
# from rest_framework import status
#
#
# @api_view(['POST'])
# def save_Contacts(request):
#     # ----- YAML below for Swagger -----
#     """
#     description: This API deletes/uninstalls a device.
#     parameters:
#       - name: Name
#         type: string
#         required: true
#         location: form
#       - name: Mobile Number
#         type: string
#         required: true
#         location: form
#       - name: Address
#         type: string
#         required: true
#         location: form
#     """
#     name = request.POST.get('Name')
#     mobile = request.POST.get('MobileNumber')
#     address = request.POST.get('Address')
#     try:
#         Contacts.objects.create(author=name, content=mobile, profile=address)
#         return Response("Data Saved!", status=status.HTTP_201_CREATED)
#     except Exception as ex:
#         return Response(ex, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def get_Contacts(request):
#     return Response(Contacts.objects.all().values(), status=status.HTTP_200_OK)
