# from rest_framework.views import APIView
import datetime

from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from pathlib import Path
from .models import ImageTable, Notes, Label
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .serializer import ImageUploadSerializer, CreateNoteSerializer, UpdateNoteSerializer, ShareSerializer, \
    LabelSerializer, \
    NotesSerializer  # , ArchieveNoteSerializer,
# TrashNoteSerializer, \
# PinnedNoteSerializer  # , SearchNoteSerializer  # NoteSerializer
# from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404, HttpResponse, request
# from django.utils.decorators import method_decorator
# from .decorators import user_login_required
# from .documents import NoteDocument
from rest_framework_jwt.settings import api_settings
from .lib.S3file import ImageUpload
import json
import os
from .lib.redisSevice import Cache
import logging
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
# pdb.set_trace()
from fundoo.settings import fh, AUTH_GITHUB_TOKEN_URL, SOCIAL_FACEBOOK_TOKEN_URL, AWS_UPLOAD_BUCKET, AWS_UPLOAD_REGION
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .lib.redisSevice import Cache
from celery.task import task
redis = Cache()
redis.__connect__()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)


class UploadFile(GenericAPIView):
    serializer_class = ImageUploadSerializer

    def responsesmd(self, success, message, data):
        response = {"status": "", "message": "", "data": "", 'status': success, 'message': message, 'data': data}
        return response

    def post(self, request):
        """
                - Posting / Uploading the data in AWS File
        """
        user = request.user
        try:
            logger.info(" Uploading file to AWS")
            file = request.FILES.get('upload')
            print(file, 'file')
            up = ImageUpload()
            response_smd = up.upload(file)
            upl = "upload"
            url = 'https://{bucket}.s3-{region}.amazonaws.com/{location}/{file}'.format(
                bucket=AWS_UPLOAD_BUCKET,
                region=AWS_UPLOAD_REGION,
                location=upl,
                file=file
            )
            Time = datetime.datetime.now()
            image = ImageTable(path=url, date=Time, filename=file, directory=upl)
            image.save()
            return HttpResponse(json.dumps(response_smd))
        except Exception as e:
            logger.info(" Data Upload Un-successfull for the user %s ", user)
            response_smd = self.responsesmd(False, "Data Upload Unsuccessfull", "")
            return HttpResponse(json.dumps(response_smd))


class LabelsCreate(GenericAPIView):
    serializer_class = LabelSerializer

    def get(self, request):
        """
            - Getting  / Printing the data of Label and the actual url for getting the data is api/note/lable
        """
        response_smd = {"success": False, "message": "Error Occured While Getting the Labels", "data": []}
        try:
            # pdb.set_trace()
            user = request.user
            redis_data = redis.hvals(str(user.id) + "label")
            print(redis_data)
            if len(redis_data) == 0:
                labels = Label.objects.filter(user_id=user.id)
                label_name = [i.label for i in labels]
                logger.info("labels where fetched from database for user :%s", request.user)
                return Response(label_name, status=200)
            logger.info("labels where fetched from redis for user :%s", request.user)
            return Response(redis_data, status=200)
        except Exception:
            logger.error("labels where not fetched for user :%s", request.user)
            return Response(response_smd, status=400)


class PostLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def post(self, request):
        """
                - Creating the Label
        """
        # pdb.set_trace()
        user = request.user
        response_smd = {"success": False, "message": "Error Occured at the Beginningg", "data": []}
        try:
            label = request.data["label"]
            if label == "":
                logger.info("Label Name was not given for %s", user)
                response_smd['message'] = "Enter Label Name"
                return Response(response_smd, status=400)
            if Label.objects.filter(user_id=user.id, label=label).exists():
                logger.info("Label Name already exists for %s", user)
                response_smd['message'] = "Label Name already exists"
                return Response(response_smd, status=400)
            else:
                newLabel = Label.objects.create(user_id=user.id, label=label)
                redis.hmset(str(user.id) + "label", {newLabel.id: label})
                # print(redis.hmset(str(user.id) + "label", {newLabel.id: label}))
                logger.info("label is created for %s", user)
                response_smd = {"success": True, "message": "Label is Created Successfully", "data": label}
                return HttpResponse(json.dumps(response_smd), status=201)
        except Exception as e:
            logger.error("%s while creating label for %s", str(e), user)
            return Response(response_smd, status=404)


class LabelsUpdate(GenericAPIView):
    serializer_class = LabelSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Label.objects.all()

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        """
                - Updating the label
        """
        label = self.get_object(pk)
        serializer = LabelSerializer(label, data=request.data)
        user = request.user
        # label_id = Label.objects.create(id=user.id)

        if serializer.is_valid():
            serializer.save()
            label = Label.objects.get(pk=pk)
            logger.info('Label is ', label)
            response_smd = {'success': True, 'message': 'Label Updated successfully.'}
            logger.info('Label Updated for the id %s in user %s', label, user)
            return Response(response_smd, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabelsDelete(GenericAPIView):
    serializer_class = LabelSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Label.objects.all()

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        """
            - Deleting the label
        """
        user = request.user
        label = self.get_object(pk)
        label.delete()
        label = Label.objects.all()
        serializer = LabelSerializer(label, many=True)
        logger.info('Label Deleted for the id %s in user %s', label, user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_user(token):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    newToken = str(token).split("Bearer ")[1]
    encodedToken = jwt_decode_handler(newToken)
    username = encodedToken['username']
    user = User.objects.get(username=username)
    return user.id


class NoteList(generics.GenericAPIView):
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        """
            - Getting  the notes that we have already created
        """
        data = Notes.objects.all()
        logger.info("Getting the Note Data on %s ", timezone.now())
        serializer = CreateNoteSerializer(data, many=True)
        page = request.GET.get('page')
        paginator = Paginator(data, 1)
        user = request.user
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            logger.warning("Got %s Error for Getting Note for User %s", str(PageNotAnInteger), user.username)
            notes = paginator.page(1)
        except EmptyPage:
            logger.warning("Got %s Error for Getting Note for User %s", EmptyPage, user)
            notes = paginator.page(paginator.num_pages)
        logger.info("All the Notes are Rendered to HTML Page for User %s", user)
        return render(request, 'pagination.html', {'notes': notes}, status=200)
        # return Response(serializer.data)


class NoteCreate(generics.GenericAPIView):
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        """
            - Creating the note
        """
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
        """
            - Getting the Archieved notes from the notes that have been created.
        """
        response_smd = {"status": False, "message": "Error Occured while Getting the Archieved Data", "data": []}
        try:
            user = request.user
            redis_data = redis.hvals(str(user.id) + "is_archived")
            tz = timezone.now()
            # print(redis_data, 'adsfadsgfadfgdfgdfagfghafgafgadfaga')
            if len(redis_data) == 0:
                response_smd = {"status": True, "message": "Your archived notes will appear here", "data": []}
                data = Notes.objects.filter(user_id=user.id, is_archived=True)
                # tz = timezone.now()
                if len(data) == 0:
                    logger.info(" Getting Inside the Archived Data ")
                    return HttpResponse(json.dumps(response_smd), status=200)
                else:
                    logger.info(" Archieve data is loaded ")
                    return HttpResponse(data.values(), status=200)
            logger.info(" Redis-Archieve data is loaded on  %s", tz)
            return HttpResponse(redis_data, status=200)
        except Exception as e:
            logger.exception("Exception Occured Archieve at %s ", e)
            return HttpResponse(json.dumps(response_smd), status=404)


class NoteReminders(GenericAPIView):

    def get(self, request):
        """
                - Getting the Reminder Data with remind and state which must require these two
        """
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
                    logger.info(" Getting Reminder Timezone %s", timezone.now())
                else:
                    state.append(reminder_list.values()[i])
                    logger.info(" Getting Reminder State  %s", state)
            reminder = {'remind': remind, 'state': state}
            logger.info(" Reminders data is loaded for %s on %s ", user, timezone.now())
            return HttpResponse(reminder.values(), status=200)
        except TypeError as e:
            logger.error("Error: %s for %s while fetching Reminder", str(e), user)
            response_smd = {"status": False, "message": "Reminder Not Set", 'data': []}
            return HttpResponse(json.dumps(response_smd), status=200)
        except Exception as e:
            logger.error("Error: %s for %s while fetching Reminder", str(e), user)
            response_smd = {"status": False, "message": "Reminder Not Set", 'data': []}
            return HttpResponse(json.dumps(response_smd), status=404)


class TrashNote(GenericAPIView):

    def get(self, request):
        """
                - Getting the Trashed notes from the notes that have been created.
        """
        response_smd = {"status": False, "message": "Error Occured while Getting the Trash Data ", "data": []}
        user = request.user
        try:
            redis_data = redis.hvals(str(user.id) + "is_trash")
            if len(redis_data) == 0:
                user = request.user
                data = Notes.objects.filter(user_id=user.id, is_trash=True)
                if len(data) == 0:
                    response = {"status": True, "message": "Trash is Empty !! "}
                    return HttpResponse(json.dumps(response_smd), status=200)
                return HttpResponse(data.values())
            return HttpResponse(redis_data)
        except Exception as e:
            return HttpResponse(json.dumps(response_smd), status=404)


class PinnedNote(GenericAPIView):

    def get(self, request):
        """
                - Getting the Pinned notes from the notes that have been created.
        """
        response_smd = {"status": False, "message": "Error Occured while Getting the Pinned Data ", "data": []}
        user = request.user
        try:
            redis_data = redis.hvals(str(user.id) + "is_pinned")
            if len(redis_data) == 0:
                user = request.user
                data = Notes.objects.filter(user_id=user.id, is_pinned=True)
                if len(data) == 0:
                    response = {"status": True, "message": " No data is Pinned !! "}
                    return HttpResponse(json.dumps(response_smd), status=200)
                return HttpResponse(data.values())
            return HttpResponse(redis_data)
        except Exception as e:
            return HttpResponse(json.dumps(response_smd), status=404)


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
        """
                        - Getting the notes based on their id the Label
        """
        note = self.get_object(pk)
        serializer = CreateNoteSerializer(note)
        return Response(serializer.data, status.HTTP_200_OK)


class NoteUpdate(GenericAPIView):
    serializer_class = UpdateNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()

    def get_object(self, pk):
        try:
            return Notes.objects.get(pk=pk)
        except Notes.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        """
                        - Updating the note based on it ID
        """
        note = self.get_object(pk)
        serializer = UpdateNoteSerializer(note, data=request.data)
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


class NoteDelete(GenericAPIView):
    serializer_class = UpdateNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()

    def get_object(self, pk):
        try:
            return Notes.objects.get(pk=pk)
        except Notes.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        """
                - Deleting the note based on its ID
        """
        note = self.get_object(pk)
        note.delete()
        notes = Notes.objects.all()
        serializer = CreateNoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NoteShare(GenericAPIView):
    serializer_class = ShareSerializer

    def post(self, request):
        """
                - Sharing the note that have been created.
        """
        response_smd = {'status': False, 'message': 'Invalid Note ', 'data': []}
        try:
            title = request.data['title']
            label = request.data['filename']
            user = request.user

            if label == "":
                return HttpResponse(json.dumps(response_smd))
            else:
                user = User.objects.get(pk=user.id)
                note_create = Notes(user_id=user.id, note=label, title=title)

                note_create.save()
                return redirect(SOCIAL_FACEBOOK_TOKEN_URL + str(title) + "\n" + str(label))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(response_smd, indent=2), status=400)


@task
def send_email(note):
    note = Notes.objects.get(pk=note)
    user = User.objects.get(pk=note.user.id)
    email = user.email
    message = " Hi, " + user.username + " you have one event today --> " + note.title
    mail_subject = 'Your Note Remainder'
    to_email = email
    send_mail(mail_subject, message, "mdhussainsabhussain@gmailcom", [to_email], fail_silently=False)
    print("mail sent")
    note.remainder = None
    note.save()

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
