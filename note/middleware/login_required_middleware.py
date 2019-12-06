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
        # print(" Came Inside Middle-Ware")
        url = request.path
        # print("Url is: ",url.split("/")[1])
        current_url = url.split("/")[1]
        print(current_url)
        # pdb.set_trace()
        if current_url == "note_api":
            print("This requires JWT authentication")
            try:
                token = request.META['HTTP_AUTHORIZATION']
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                new_token = str(token).split("Bearer ")[1]
                print("Token Generated is", new_token)
                encoded_token = jwt_decode_handler(new_token)
                print(encoded_token)
                username = encoded_token['username']
                print(username)
                user = User.objects.get(username=username)
                try:
                    if user and user.is_active:
                        print("Autorized User")
                        pass
                except User.DoesNotExist:
                    responsesmd = {'status': False, 'message': 'Authentication Required'}
                    return HttpResponse(json.dumps(responsesmd), status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                if request.session:
                    user = request.user
                    if user.is_authenticated:
                        pass
                    else:
                        responsesmd  = {'status': False, 'message': 'Users credential not provided..!!'}
                        return HttpResponse(json.dumps(responsesmd), status=status.HTTP_400_BAD_REQUEST)
                else:
                    responsesmd = {'status': False, 'message': 'Users credential not provided..!!'}
                    return HttpResponse(json.dumps(responsesmd), status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Doesn't Require JWT Authentication")
        return self.get_response(request)
