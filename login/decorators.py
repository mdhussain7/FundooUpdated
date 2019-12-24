import jwt,re
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from rest_framework.views import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def login_decorator(function):
    """
    :param function: function is called
    :return: will check token expiration
    """
    # permission_classes = (IsAuthenticated,)

    def wrapper(request,*args, **kwargs):
        """
        :return: will check token expiration
        """
        username = request.user
        return function(request,*args, **kwargs)
    return wrapper


