# from rest_framework.views import APIView
import datetime
import pdb

from django.utils import timezone
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
    PinnedNoteSerializer  # , SearchNoteSerializer  # NoteSerializer
# from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404, HttpResponse, request
# from django.utils.decorators import method_decorator
# from .decorators import user_login_required
# from .documents import NoteDocument
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .lib.S3file import ImageUpload
import json
import os
from .lib.redis import RedisOperation
import logging

# pdb.set_trace()
from fundoo.settings import fh

# print(fh)
env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

Ro = RedisOperation()
redis = Ro.server
# logger = logging.getLogger(__name__) fh = logging.FileHandler('fundoo.log') formatter= logging.Formatter('[%(
# asctime)s] - %(name)s - %(levelname)- %(message)s - p%(process)s {%(pathname)s:%(lineno)d} % ','%m-%d %H:%M:%S')
# fh.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)


class UploadFile(GenericAPIView):
    serializer_class = ImageUploadSerializer

    def responsesmd(self, success, message, data):
        response = {"status": "", "message": "", "data": "", 'status': success, 'message': message, 'data': data}
        return response

    def post(self, request):
        try:
            logger.info(" Want to Upload an image \n Please Select any ...")
            file = request.FILES.get('upload')
            print(file, 'file')
            up = ImageUpload()
            smdresponse = up.upload(file)
            upl = "upload"
            AWS_UPLOAD_BUCKET = os.getenv('AWS_UPLOAD_BUCKET')
            AWS_UPLOAD_REGION = os.getenv('AWS_UPLOAD_REGION')
            url = 'https://{bucket}.s3-{region}.amazonaws.com/{location}/{file}'.format(
                bucket=AWS_UPLOAD_BUCKET,
                region=AWS_UPLOAD_REGION,
                location=upl,
                file=file
            )
            Time = datetime.datetime.now()
            image = ImageTable(path=url, date=Time, filename=file, directory=upl)
            image.save()
            return HttpResponse(json.dumps(smdresponse))
        except Exception as e:
            smdresponse = self.responsesmd(False, "Data Upload Unsuccessfull", "")
            return HttpResponse(json.dumps(smdresponse))


def get_user(token):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    newToken = str(token).split("Bearer ")[1]
    # print("Token Created is: ", newToken)
    encodedToken = jwt_decode_handler(newToken)
    # print(encodedToken)
    username = encodedToken['username']
    # print(username)
    user = User.objects.get(username=username)
    return user.id


class NoteList(generics.GenericAPIView):
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        contact = Notes.objects.all()
        logger.info("Getting the Note Data on %s ", timezone.now() )
        serializer = CreateNoteSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        user = request.user
        response = {"status": False, "message": "Invalid Response", "data": []}
        title = request.data["title"]
        description = request.data["description"]
        tz = timezone.now()
        if Notes.objects.filter(user_id=user.id, title=title, description=description).exists():
            logger.info('Note already exists for %s Time is %s', user, tz)
            response['message'] = "Note already exists"
            return Response(response, status=400)
        else:
            noteCreated = Notes.objects.create(user_id=user.id, title=title, description=description)
            result = Notes.objects.values()

            list_result = [i for i in result]
            redis.hmset(str(user.id) + "Note", {noteCreated.id: list_result})

            logger.info("Note is created for %s Time is %s", user, tz)
            response = {"status": True, "message": "Note is Created", "data": title}
            return HttpResponse(json.dumps(response), status=201)


class ArchieveNote(GenericAPIView):
    def get(self, request):
        try:
            response = {"status": False, "message": "Error Occured while Getting the Archieved Data", "data": []}
            user = request.user
            redis_data = redis.hvals(str(user.id) + "is_archived")
            tz = timezone.now()
            # print(redis_data, 'adsfadsgfadfgdfgdfagfghafgafgadfaga')
            if len(redis_data) == 0:
                response = {"status": True, "message": "Your archived notes will appear here", "data": []}
                data = Notes.objects.filter(user_id=user.id, is_archived=True)
                tz  = timezone.now()
                if len(data) == 0:
                    logger.info(" Getting Inside the Archived Data %s", tz)
                    return HttpResponse(json.dumps(response), status=200)
                else:
                    logger.info(" Archieve data is loaded %s", tz)
                    return HttpResponse(data.values(), status=200)
            logger.info(" Redis-Archieve data is loaded on  %s", tz)
            return HttpResponse(redis_data, status=200)
        except Exception as e:
            return HttpResponse(json.dumps(response), status=404)


class NoteReminders(GenericAPIView):

    def get(self, request):
        # pdb.set_trace()
        user = request.user
        try:
            reminder_data = Notes.objects.filter(user_id=user.id)
            reminder_list = reminder_data.values_list('reminder', flat=True)
            remind = []
            state = []
            logger.info(" Getting Inside the Reminder Data ")
            for i in range(len(reminder_list.values())):
                if reminder_list.values()[i]['reminder'] is None:
                    # logger.info(" Getting Reminder Data %s", reminder_list.values()[i]['reminder'])
                    continue
                elif timezone.now() > reminder_list.values()[i]['reminder']:
                    remind.append(reminder_list.values()[i])
                    logger.info(" Getting Reminder Timezone %s", timezone.now() )
                else:
                    state.append(reminder_list.values()[i])
                    logger.info(" Getting Reminder State  %s", state)

            reminder = {
                'remind': remind,
                'state': state
            }
            logger.info(" Reminders data is loaded for %s on %s ", user , timezone.now() )
            return HttpResponse(reminder.values(), status=200)
        except TypeError as e:
            logger.info("Error: %s for %s while fetching Reminder", str(e), user)
            responessmd = {"status": False, "message": "Reminder Not Set", 'data': []}
            return HttpResponse(json.dumps(responessmd), status=200)
        except Exception as e:
            logger.info("Error: %s for %s while fetching Reminder", str(e), user)
            responessmd = {"status": False, "message": "Reminder Not Set", 'data': []}
            return HttpResponse(json.dumps(responessmd), status=404)


class TrashNote(GenericAPIView):
    def get(self, request):
        response = {"status": False, "message": "Error Occured while Getting the Trash Data ", "data": []}
        user = request.user
        try:
            redis_data = redis.hvals(str(user.id) + "is_trash")
            if len(redis_data) == 0:
                user = request.user
                data = Notes.objects.filter(user_id=user.id, is_trash=True)
                if len(data) == 0:
                    response = {"status": True, "message": "Trash is Empty !! "}
                    return HttpResponse(json.dumps(response), status=200)
                return HttpResponse(data.values())
            return HttpResponse(redis_data)
        except Exception as e:
            return HttpResponse(json.dumps(response), status=404)


class PinnedNote(GenericAPIView):
    def get(self, request):
        response = {"status": False, "message": "Error Occured while Getting the Pinned Data ", "data": []}
        user = request.user
        try:
            redis_data = redis.hvals(str(user.id) + "is_pinned")
            if len(redis_data) == 0:
                user = request.user
                data = Notes.objects.filter(user_id=user.id, is_pinned=True)
                if len(data) == 0:
                    response = {"status": True, "message": " No data is Pinned !! "}
                    return HttpResponse(json.dumps(response), status=200)
                return HttpResponse(data.values())
            return HttpResponse(redis_data)
        except Exception as e:
            return HttpResponse(json.dumps(response), status=404)


class NoteDetails(GenericAPIView):
    serializer_class = UpdateNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()

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
            logger.info('Note is ', note)
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
