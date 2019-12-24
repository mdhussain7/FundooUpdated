# from rest_framework.views import APIView
import datetime
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .decorators import user_login_required
import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from pathlib import Path
from .models import ImageTable, Notes, Label
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .serializer import ImageUploadSerializer, CreateNoteSerializer, UpdateNoteSerializer, ShareSerializer, \
    LabelSerializer, ReminderNoteSerializer, SearchNoteSerializer, NotesSerializer, \
    NotesDocumentSerializer  # , ArchieveNoteSerializer,

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404, HttpResponse, request, BadHeaderError
# from django.utils.decorators import method_decorator
# from .decorators import user_login_required
from .documents import NoteDocument
from rest_framework_jwt.settings import api_settings
from .lib.S3file import ImageUpload
import json
import os
import logging
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
# pdb.set_trace()
from fundoo.settings import fh, AUTH_GITHUB_TOKEN_URL, SOCIAL_FACEBOOK_TOKEN_URL, AWS_UPLOAD_BUCKET, AWS_UPLOAD_REGION, \
    EMAIL_HOST_USER
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .lib.redisSevice import Cache

redis = Cache()
connection = redis.__connect__()

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
            # print(file, 'file')
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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
class PostLabel(GenericAPIView):
    serializer_class = LabelSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Label.objects.all()

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

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

    def put(self, request, pk):
        """
                - Updating the label
        """
        label = self.get_object(pk)
        serializer = LabelSerializer(label, data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save()
            label = Label.objects.get(pk=pk)
            logger.info('Label is ', label)
            response_smd = {'success': True, 'message': 'Label Updated successfully.'}
            logger.info('Label Updated for the id %s in user %s', label, user)
            return Response(response_smd, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
class NoteCreate(generics.GenericAPIView):
    serializer_class = CreateNoteSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        """
            - Getting  the notes that we have already created
        """
        data = Notes.objects.all()
        logger.info("Getting the Note Data on %s ", timezone.now())
        # serializer = CreateNoteSerializer(data, many=True)
        page = request.GET.get('page')
        paginator = Paginator(data, 1)
        user = request.user
        try:
            notes = paginator.page(page)
        except PageNotAnInteger as pni:
            logger.warning("Got %s Error for Getting Note for User %s", str(pni), user.username)
            notes = paginator.page(1)
        except EmptyPage as ep:
            logger.warning("Got %s Error for Getting Note for User %s", ep, user)
            notes = paginator.page(paginator.num_pages)
        logger.info("All the Notes are Rendered to HTML Page for User %s", user)
        return render(request, 'pagination.html', {'notes': notes}, status=200)
        # return Response(serializer.data)

    @staticmethod
    def post(request):
        """
                - Creating the note
        """
        user = request.user
        try:
            data = request.data
            if len(data) == 0:
                raise KeyError
            user = request.user
            collaborator_list = []
            try:
                data["label"] = [Label.objects.filter(user_id=user.id, label=label).values()[0]['id'] for label in
                                 data["label"]]
            except KeyError:
                logger.debug('label was not added by the user %s', user)
                pass
            try:
                collaborator = data['collaborate']
                for email in collaborator:
                    email_id = User.objects.filter(email=email)
                    user_id = email_id.values()[0]['id']
                    collaborator_list.append(user_id)
                data['collaborate'] = collaborator_list
                print(data['collaborate'])
            except KeyError:
                logger.debug('collaborator was not added by the user %s', user)
                pass
            serializer = NotesSerializer(data=data, partial=True)
            if serializer.is_valid():
                note_create = serializer.save(user_id=user.id)
                response = {'success': True, 'message': "note created", 'data': []}
                if serializer.data['is_archived']:
                    redis.hmset(str(user.id) + "is_archived",
                                {note_create.id: str(json.dumps(serializer.data))})  # created note is cached in redis
                    logger.info("note is created for %s with note id as %s", user, note_create.id)
                    return HttpResponse(json.dumps(response, indent=2), status=201)
                else:
                    if serializer.data['reminder']:
                        redis.hmset("reminder",
                                    {note_create.id: str(json.dumps({"email": user.email, "user": str(user),
                                                                     "note_id": note_create.id,
                                                                     "reminder": serializer.data["reminder"]}))})
                    redis.hmset(str(user.id) + "note",
                                {note_create.id: str(json.dumps(serializer.data))})

                    logger.info("Note is created for %s with note data as %s", user, note_create.__repr__())
                    return HttpResponse(json.dumps(response, indent=2), status=201)
            logger.error(" %s for  %s", user, serializer.errors)
            response = {'success': False, 'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except KeyError as e:
            logger.error("Got %s error for creating note as no data was provided for user %s", str(e), user)
            response = {'success': False, 'message': "one of the field is empty ", 'data': []}
            return Response(response, status=400)
        except Exception as e:
            logger.error("Got %s error for creating note for user %s", str(e), user)
            response = {'success': False, 'message': "something went wrong", 'data': []}
            return Response(response, status=400)

    # def post(self, request, format=None):
    #     """
    #         - Creating the note
    #     """
    #     user = request.user
    #     response = {"status": False, "message": "Invalid Response", "data": []}
    #     title = request.data["title"]
    #     description = request.data["description"]
    #     tz = timezone.now()
    #     # if Notes.objects.filter(user_id=user.id, title=title, description=description).exists():
    #     #     logger.info('Note already exists for %s Time is %s', user, tz)
    #     #     response['message'] = "Note already exists"
    #     #     return Response(response, status=400)
    #     # else:
    #     noteCreated = Notes.objects.create(user_id=user.id, title=title, description=description)
    #
    #     result = Notes.objects.values()
    #     list_result = [i for i in result]
    #     redis.hmset(str(user.id) + "Note", {noteCreated.id: list_result})
    #     logger.info("Note is created for %s Time is %s", user, tz)
    #     response = {"status": True, "message": "Note is Created", "data": title}
    #     return HttpResponse(json.dumps(response), status=201)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
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

    def delete(self, request, pk):
        """
                - Deleting the note based on its ID
        """
        note = self.get_object(pk)
        note.delete()
        notes = Notes.objects.all()
        serializer = CreateNoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
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
                elif timezone.localtime() > reminder_list.values()[i]['reminder']:
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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
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
                    response_smd = {"status": True, "message": "Trash is Empty !! "}
                    # return HttpResponse(json.dumps(response_smd), status=200)
                # return HttpResponse(data.values())
            # return HttpResponse(redis_data)
            return HttpResponse(json.dumps(response_smd), status=200)
        except Exception as e:
            return HttpResponse(json.dumps(response_smd), status=404)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
class PinnedNote(GenericAPIView):

    def get(self, request):
        """
                - Getting the Pinned notes from the notes that have been created.
        """
        response_smd = {"status": False, "message": "Error Occured while Getting the Pinned Data ", "data": []}
        user = request.user
        try:
            if connection:
                redis_data = redis.hvals(str(user.id) + "is_pinned")
                if len(redis_data) == 0:
                    user = request.user
                    data = Notes.objects.filter(user_id=user.id, is_pinned=True)
                    if len(data) == 0:
                        response_smd = {"status": True, "message": " No data is Pinned !! "}
                        return HttpResponse(json.dumps(response_smd), status=200)
                    return HttpResponse(data.values())
                return HttpResponse(redis_data)
        except Exception as e:
            return HttpResponse(json.dumps(response_smd), status=404)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
class Celery(GenericAPIView):
    serializer_class = ReminderNoteSerializer

    def get(self, request):
        """
            - Summary:
            - Celery class works on clery beat and every 30 sec this end point is hit.
            - Methods:
            - Get: this method where logic is written for triggering reminders notification service where
            - Email is sent if reminder time matched with current time.
        """
        try:
            # import pdb
            # pdb.set_trace()
            response = {"success": False, "message": "Error Occured While Getting the Reminder Note", "data": []}
            reminder = Notes.objects.filter(reminder__isnull=False)
            startTime = timezone.localtime() - timedelta(minutes=5)
            endTime = timezone.localtime() + timedelta(minutes=5)
            try:
                for i in range(len(reminder)):
                    if startTime <= reminder.values()[i]['reminder'] <= endTime:
                        user_id = reminder.values()[i]['user_id']
                        user = User.objects.get(id=user_id)
                        subject = 'Reminder Notification From Fundoo'
                        html_message = render_to_string('reminder.html', {'user': user})
                        plain_message = strip_tags(html_message)
                        mail.send_mail(subject, plain_message, EMAIL_HOST_USER, ['srmsa786@gmail.com'],
                                       html_message=html_message)
                        response = {"success": True, "message": "Email Sent", "data": []}
                        logger.info("Email Successfully Sent %s ", user)
                    return HttpResponse(json.dumps(response))
            except Exception as e:
                logger.info("exception %s", str(e))
                return HttpResponse(json.dumps(response))
        except  Exception as e:
            logger.info(str(e))


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_login_required, name='dispatch')
class SearchNote(GenericAPIView):
    serializer_class = SearchNoteSerializer
    parser_classes = FormParser, JSONParser, MultiPartParser
    data = Notes.objects.all()

    def post(self, request):
        # import pdb
        # pdb.set_trace()
        response_smd = {"success": False, "message": "Error Occured at the Beginning", "data": []}
        try:
            search_title = request.data['title']
            if search_title:
                notes = NoteDocument.search().query("multi_match", query=search_title, fields=['title'])
                if notes.count() == 0:
                    response_smd = {'status': False, 'message': "No Search Results Found ..!!"}
                    return HttpResponse(json.dumps(response_smd))
                serializer = SearchNoteSerializer(notes, many=True)
                logger.info("Total Number of Search Results are %s for the search %s ", notes.count(), search_title)
                return Response(serializer.data, status=200)
            else:
                logger.error(" Error Occcured while Fetching the Note")
                return HttpResponse(json.dumps(response_smd, indent=2), status=400)
        except Exception as e:
            logger.error(str(e))
            return HttpResponse(json.dumps(response_smd), status=400)
