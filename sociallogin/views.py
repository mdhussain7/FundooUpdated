from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateNotesSerializer
from .models import CreateNotes, LoggedInUser
from django.http import HttpResponse


# Create your views here.
class SocialUser(APIView):
    def get(self, request):
        content = {'message': 'Social User'}
        return Response(content)


class ViewData(GenericAPIView):
    serializer_class = CreateNotesSerializer

    def get_queryset(self):
        return

    def get(self, request):
        notes = CreateNotes.objects.all()
        serializer = CreateNotesSerializer(notes, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        try:
            print("Into the Post")
            users = User.objects.select_related('logged_in_user')
            print("After Users",users)
            username = request.user
            print(username)
            for user in users:
                user.status = 'Online' if hasattr(user, 'logged_in_user') else 'off-line'
            loggedusers = LoggedInUser.objects.all()  # new
            return HttpResponse(render(request, 'social.html',
                                       {'online user': loggedusers,
                                        'users': users,
                                        'username': username
                                        }
                                       ))
            # return HttpResponse(render(request,'social.html'))
        except Exception as e:
            print("Exception", e)
            return HttpResponse(render(request,'/'))


