import jwt, re
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

csrf_protected_method = method_decorator(csrf_protect)
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def login_decorator(function):
    def wrapper(request, *args, **kwargs):
        username = request.user
        print(username)
        content = {'message': 'Hi,'}
        return function(request, *args, **kwargs)

        return Response(content)
        red = Redis()  # red object is created
        token = red.get('token').decode("utf-8")
        print(token)

        user1 = decode['username']
        user2 = User.objects.get(username=user1)
        if user2 is not None:
            print("hello")
            return function(request, *args, **kwargs)
    return wrapper
