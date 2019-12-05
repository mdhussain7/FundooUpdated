# from rest_framework.views import APIView
import datetime

from rest_framework.permissions import IsAuthenticated

from .serializer import ImageUploadSerializer
# from rest_framework import permissions, status, authentication
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .config_aws import (
#     AWS_UPLOAD_BUCKET,
#     AWS_UPLOAD_REGION,
#     AWS_UPLOAD_ACCESS_KEY_ID,
#     AWS_UPLOAD_SECRET_KEY
# )
# from .models import FileItem
from dotenv import load_dotenv
from pathlib import Path
from .models import ImageTable, Notes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .serializer import CreateNoteSerializer, UpdateNoteSerializer, ArchieveNoteSerializer, TrashNoteSerializer, \
    PinnedNoteSerializer # , SearchNoteSerializer  # NoteSerializer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404, HttpResponse, request
# from django.utils.decorators import method_decorator
# from .decorators import user_login_required
# from .documents import NoteDocument
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
# import json
from .lib.S3file import ImageUpload
import json
import os
from .lib.redis import RedisOperation

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

Ro = RedisOperation()
redis = Ro.server


class UploadFile(GenericAPIView):
    serializer_class = ImageUploadSerializer

    def responsesmd(self, success, message, data):
        print("Inside Respoinse SMD")
        response = {"status": "", "message": "", "data": "", 'status': success, 'message': message, 'data': data}
        print("After Response")
        return response

    def post(self, request):
        try:
            print(" Want to Upload an image \n Please Select any ...")
            file = request.FILES.get('upload')
            print(file, 'file')
            up = ImageUpload()
            smdresponse = up.upload(file)
            print("SMD Call")
            print(smdresponse)
            print(file)
            upl = "upload"
            AWS_UPLOAD_BUCKET = os.getenv('AWS_UPLOAD_BUCKET')
            AWS_UPLOAD_REGION = os.getenv('AWS_UPLOAD_REGION')
            url = 'https://{bucket}.s3-{region}.amazonaws.com/{location}/{file}'.format(
                bucket=AWS_UPLOAD_BUCKET,
                region=AWS_UPLOAD_REGION,
                location=upl,
                file=file
            )
            print(url)
            Time = datetime.datetime.now()
            print(Time)
            image = ImageTable(path=url, date=Time, filename=file, directory=upl)
            print(image)
            image.save()
            # smdresponse = self.smd_response(True, 'Data Inserted Successfully into the Database', '')
            return HttpResponse(json.dumps(smdresponse))
        except Exception as e:
            print("Exception", e)
            smdresponse = self.responsesmd(False, "Data Upload Unsuccessfull", "")
            # smdresponse = "Failed Uploading"
            return HttpResponse(json.dumps(smdresponse))


def get_user(token):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    newToken = str(token).split("Bearer ")[1]
    print("Token Created is: ", newToken)
    encodedToken = jwt_decode_handler(newToken)
    print(encodedToken)
    username = encodedToken['username']
    print(username)
    user = User.objects.get(username=username)
    return user.id


# @method_decorator(user_login_required, name='dispatch')
# class NoteList(APIView):
#     serializer_class = CreateNoteSerializer
#     parser_classes = FormParser, JSONParser, MultiPartParser
#
#     # permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         notes = Notes.objects.all()
#         serializer = CreateNoteSerializer(notes, many=True)
#         return Response(serializer.data, status=200)
#
#     def post(self, request, format=None):
#         serializer = CreateNoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# def post(self, request):
#     # print(request.META)
#     # token = request.META['HTTP_AUTHORIZATION']
#     # print(token)
#     # # print(request.META)
#     # # token="qqq"
#     # user = get_user(token)
#     # request.data._mutable = True
#     # request.data['user'] = user
#     data = request.data
#
#     serializer = CreateNoteSerializer(data=data)
#     print(serializer.data)
#     if serializer.is_valid():
#         serializer.save()
#         responsesmd = {'status': True, 'message': 'Hurray Note Successfully Created'}
#         return Response(responsesmd, status=201)
#     return Response(serializer.errors, status=400)


class NoteList(generics.GenericAPIView):
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        contact = Notes.objects.all()
        serializer = CreateNoteSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CreateNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(user_login_required, name='dispatch')
class ArchieveNote(GenericAPIView):
    serializer_class = ArchieveNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()
    print("Database ", "Data ", "", data)

    def get(self, request):
        serializer = ArchieveNoteSerializer(self.data, many=True)
        print(serializer.data)
        if serializer.data[2]:
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrashNote(GenericAPIView):
    serializer_class = TrashNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()
    print("Database ", data)
    # user = request.user

    # def get(self, request):
        # trash = Notes.objects.filter(used_id=user, trash=is_trash)
        # print(serializer.data)
        # if trash:
        #     return Response(trash, status.HTTP_200_OK)
        # else:
        #     return Response(trash.errors, status=status.HTTP_400_BAD_REQUEST)


class PinnedNote(GenericAPIView):
    serializer_class = PinnedNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()
    print("Database ", "Data ", "", data)

    def get(self, request):
        serializer = PinnedNoteSerializer(self.data, many=True)
        print(serializer.data)
        print()
        print()
        # pin = []
        for ispinned in serializer.data:
            key = ispinned
            # print(dir(dict()))
            k = dict(key)
            key = k.items()
            # key = str(list(key)).strip("OrderedDict()")
            # print(type(key))
            print(key)
            if key is 'is_pinned':
                print(key)
                # for value in key:
                #     val = value
                #     if val is not True:
                #         print(val)
                #         for v in val:
                #             va = v
                #             if va is not True:
                #                 print(va)
        # for i in serializer.data:
        # print(pin.append(i))
        # print()
        # print(i)
        # print()
        # print()
        # print(pin)
        # for j in i:
        #     print(j[0])
        # if j:
        #     print(j)
        # if i['is_pinned']==j['True']:
        #     print(i,j)
        # print()
        # print()
        # print(serializer.data[1])
        # print(dir(serializer.data))
        # print(serializer.data.__contains__)
        # if serializer.data.__getattribute__ == 'is_pinned':
        #     print("Somethuing")
        if serializer.data:
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.data, status.HTTP_200_OK)


class NoteDetails(GenericAPIView):
    serializer_class = UpdateNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()
    print("Database ", "Data ", "", data)

    def get_object(self, pk):
        try:
            return Notes.objects.get(pk=pk)
        except Notes.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = CreateNoteSerializer(note)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = UpdateNoteSerializer(note, data=request.data)
        # note_id = Notes.objects.create(id=user.id)
        if serializer.is_valid():
            serializer.save()
            note = Notes.objects.get(pk=pk)
            print('Note is ', note)
            if note.is_archived:
                note.is_pinned = False
                note.save()
            responsesmd = {'success': True, 'message': 'Note Updated successfully.'}
            return Response(responsesmd, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        notes = Notes.objects.all()
        serializer = CreateNoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SearchNote(APIView):
#
#     def get(self, request):
#         search_data = request.GET.get('search_data')
#         if search_data:
#             notes = NoteDocument.search().query("multi_match", query=search_data, fields=["title", "description"])
#
#         if notes.count() == 0:
#             responsesmd = {'success': False, 'message': "No Search results found ..!!"}
#             return HttpResponse(json.dumps(responsesmd))
#
#         print("Total Search Results", notes.count())
#         serializer = SearchNoteSerializer(notes, many=True)
#         return Response(serializer.data, status=200)
