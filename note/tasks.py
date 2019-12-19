import requests
from django.contrib.auth.models import User
from urllib3.util import url

from .models import Notes
from celery.task import task
import datetime
from celery import Celery, shared_task
from django.core.mail import send_mail
import logging
from fundoo.settings import fh, BASE_URL ,CELERY_API_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
app = Celery()
app.conf.timezone = 'Asia/Kolkata'
@task
def sent_mail():
    requests.get(url=BASE_URL+CELERY_API_URL)
from django.contrib.auth.models import User
from .models import Notes
from celery.task import task
import datetime
from celery import Celery
from django.core.mail import send_mail

# app = Celery()


# @task
# def get_remainders():
#     now = datetime.datetime.now()
#     print("current date and time --->", now)
#     notes = Notes.objects.exclude(reminder=None)
#     print("length ===>>", len(notes))
#     for i in range(len(notes)):
#         five_min_before_reminder_time = notes[i].reminder.replace(tzinfo=None) - datetime.timedelta(minutes=1)
#         if five_min_before_reminder_time >= now and now <= notes[i].reminder.replace(tzinfo=None):
#             """
#             pass the remainders on queue
#             """
#             send_email.delay(notes[i].id)
#
# @task
# def send_email(note):
#     note = Notes.objects.get(pk=note)
#     user = User.objects.get(pk=note.user.id)
#     email = user.email
#     message = " Hi, " + user.username + " you have one event today --> " + note.title
#     mail_subject = 'Your Note Remainder'
#     to_email = email
#     send_mail(mail_subject, message, "mdhussainsabhussain@gmailcom", [to_email], fail_silently=False)
#     print("mail sent")
#     note.remainder = None
#     note.save()