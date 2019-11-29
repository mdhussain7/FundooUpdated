from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateNotesSerializer
from .models import CreateNotes
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
            # print("Inside Post")
            # title = CreateNotes.title
            # print("Title")
            # content = CreateNotes.content
            # print("After Content")
            # file = CreateNotes.filename
            # print("File")
            # dataPost = CreateNotes(title=title, content=content, filename=file)
            # print(dataPost)
            # dataPost.save()
            return HttpResponse(render(request,'social.html'))
        except Exception as e:
            print("Exception", e)
            return HttpResponse(render(request,'/'))


