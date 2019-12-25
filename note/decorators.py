from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponse
import json


def user_login_required(view_func):
    def wrapper(request, *args,**kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            # token = "@@@"
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            new_token = str(token).split("Bearer ")[1]
            encoded_token = jwt_decode_handler(new_token)
            username = encoded_token['username']
            user = User.objects.get(username=username)
            try:
                if user and user.is_active:
                    return view_func(request, *args, **kwargs)
            except User.DoesNotExist:
                response_smd = {'status': False, 'message': 'Login is required'}
                return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
        except KeyError :
            if request.session:
                user = request.user
                if user.is_authenticated:
                    return view_func(request, *args, **kwargs)
                else:
                    response_smd = {'status': False, 'message': 'Enter the Proper Credentials!!'}
                    return HttpResponse(json.dumps(response_smd),  status=status.HTTP_400_BAD_REQUEST)
            else:
                response_smd = {'status': False, 'message': 'Enter the Proper Credentials!!'}
                return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
    return wrapper
