# from django.contrib.auth.models import User
# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.generics import GenericAPIView
import json

from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateSocialSerializer, ShareSerializer
from .models import CreateSocial, LoggedInUser
# from django.http import HttpResponse
# import pdb
from django.contrib import auth
# from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from authlib.integrations.requests_client import OAuth2Session
from rest_framework.generics import GenericAPIView
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
AUTH_GITHUB_URL = os.getenv('AUTH_GITHUB_URL')
AUTH_GITHUB_TOKEN_URL = os.getenv('AUTH_GITHUB_TOKEN_URL')
BASE_URL = os.getenv('BASE_URL')
AUTH_GITHUB_USER_EMAIL_URL = os.getenv('AUTH_GITHUB_USER_EMAIL_URL')
AUTH_GITHUB_USER_URL = os.getenv('AUTH_GITHUB_USER_URL')
SOCIAL_FACEBOOK_TOKEN_URL = os.getenv('SOCIAL_FACEBOOK_TOKEN_URL')
# file_handler = os.getenv('file_handler')
# logging = os.getenv('logging')

from .redis import RedisOperation
from .token import token_validation
from .models import SocialLogin

Ro = RedisOperation()
red = Ro.red


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(file_handler)


# Create your views here.
class SocialUser(APIView):
    def get(self, request):
        content = {'message': 'Social User'}
        return Response(content)


class ViewData(GenericAPIView):
    serializer_class = CreateSocialSerializer

    def get_queryset(self):
        return

    def get(self, request):
        notes = CreateSocial.objects.all()
        serializer = CreateSocialSerializer(notes, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        try:
            # print("Into the Social Post")
            # users = User.objects.select_related('logged_in_user')
            # print("After Users :",users)
            # username = request.user
            # print(username)
            # for user in users:
            #     user.status = 'Online' if hasattr(user, 'logged_in_user') else 'off-line'
            # loggedusers = LoggedInUser.objects.all()  # new
            # return HttpResponse(render(request, 'social.html',
            #                            {'online user': loggedusers,
            #                             'users': users,
            #                             'username': username
            #                             }
            #                            ))
            # serializer = CreateSocialSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(render(request, 'social.html'))
        except Exception as e:
            print("Exception", e)
            return HttpResponse(render(request, '/'))


class Github(GenericAPIView):

    def get(self, request):
        # pdb.set_trace()
        resp = {'success': False, 'message': "Something Went Wrong and an Un-expected Error Occured", 'data': []}
        try:
            auth_url = AUTH_GITHUB_URL
            scope = 'user:email'
            client = OAuth2Session(SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, scope=scope)
            url, state = client.create_authorization_url(auth_url)
            print("Redirected user to Github Login page", )
            return redirect(url)
        except Exception as e:
            # logger.error("got %s error while redirecting the user to github login page ", str(e))
            return HttpResponse(resp, status=404)


class GitHubAuthenticator(GenericAPIView):

    def get(self, request):

        smdresp = {'success': False, 'message': "Something Went Wrong", 'data': []}
        try:
            # pdb.set_trace()
            urlToken = AUTH_GITHUB_TOKEN_URL  # github token url.
            scope = 'user:email'
            client = OAuth2Session(SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, scope=scope)

            token = client.fetch_token(urlToken, client_id=SOCIAL_AUTH_GITHUB_KEY,
                                       client_secret=SOCIAL_AUTH_GITHUB_SECRET
                                       , authorization_response=BASE_URL + request.get_full_path())
            client = OAuth2Session(SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, token=token, scope=scope)
            account_url_email = AUTH_GITHUB_USER_EMAIL_URL
            account_url = AUTH_GITHUB_USER_URL

            response = client.get(account_url)
            response_email = client.get(account_url_email)

            user_details = response.json()
            email_id = response_email.json()[0]["email"]
            username = response.json()["login"]
            first_name = user_details["name"].split(" ")[0]
            last_name = user_details["name"].split(" ")[1]

            if SocialLogin.objects.filter(unique_id=response.json()["id"]).exists():
                user = auth.authenticate(username=username, password=response.json()["id"])
                token = token_validation(user.username, response.json()["id"])
                auth.login(request, user)
                red.set(user.username, token)
                print("%s Logged in using Social auth ", user.username)
                return redirect("/notes/")
            else:
                SocialLogin.objects.create(unique_id=response.json()["id"], provider="github",
                                           full_name=user_details["name"],
                                           username=username, EXTRA_PARAMS=response.json())
                if User.objects.filter(username=username).exists():

                    user = User.objects.create_user(username=response.json()["id"], first_name=first_name,
                                                    last_name=last_name,
                                                    email=email_id, password=response.json()["id"])
                    user.save()
                    token = token_validation(username, response.json()["id"])
                    red.set(user.username, token)
                    print("%s logged in as well as user got registered but username already exist so his id is as his "
                          "username ", user.username)
                else:
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                    email=email_id, password=response.json()["id"])
                    user.save()
                    token = token_validation(username, response.json()["id"])
                    red.set(user.username, token)
                    print("%s Logged in as well as user got Registered ", user.username)
            return redirect("/notes/")
        except Exception as e:
            print("Exception Occured ", e)
            return HttpResponse(smdresp, status=404)


class NoteShare(GenericAPIView):
    serializer_class = ShareSerializer

    def post(self, request):
        responsesmd = {'success': False, 'message': 'Invalid Note ', 'data': []}
        try:
            title = request.data['title']
            note = request.data['filename']
            user = request.user

            if note == "":
                return HttpResponse(json.dumps(responsesmd))
            else:
                user = User.objects.get(pk=user.id)
                note_create = CreateSocial(user_id=user.id, note=note, title=title)

                note_create.save()
                return redirect(AUTH_GITHUB_TOKEN_URL + str(title) + "\n" + str(note))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(responsesmd, indent=2), status=400)
