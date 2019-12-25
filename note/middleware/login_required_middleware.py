# import pdb
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponse
import json


class LoginRequired(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.path
        current_url = url.split("/")[1]
        if current_url == "api":
            try:
                token = request.META['HTTP_AUTHORIZATION']
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                new_token = str(token).split("Bearer ")[1]
                encoded_token = jwt_decode_handler(new_token)
                username = encoded_token['username']
                user = User.objects.get(username=username)
                try:
                    if user and user.is_active:
                        pass
                except User.DoesNotExist:
                    response_smd = {'status': False, 'message': 'Authentication Required'}
                    return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                if request.session:
                    user = request.user
                    if user.is_authenticated:
                        pass
                    else:
                        response_smd  = {'status': False, 'message': 'Users credential not provided..!!'}
                        return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
                else:
                    response_smd = {'status': False, 'message': 'Users credential not provided..!!'}
                    return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.get_response(request)
