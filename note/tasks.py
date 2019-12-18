from django.contrib.auth.models import User
from .models import Notes
from celery.task import task
import datetime
from celery import Celery, shared_task
from django.core.mail import send_mail
import logging
from fundoo.settings import fh

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
app = Celery()

@task
def get_reminders():
    current = datetime.datetime.now()
    # logger.info("Current Time", current)
    reminderData = Notes.objects.exclude(reminder=None)
    # logger.info(" Note Length ", len(reminderData))
    for i in range(len(reminderData)):
        data_before_reminder_time = reminderData[i].reminder.replace(tzinfo=None) - datetime.timedelta(minutes=1)
        if data_before_reminder_time >= current and current <= reminderData[i].reminder.replace(tzinfo=None):
            """
                - Reminders One by One
            """
            sendEmail.delay(reminderData[i].id)


@task
def sendEmail(note):
    note = Notes.objects.get(pk=note)
    user = User.objects.get(pk=note.user.id)
    email = user.email
    message = " Hi, " + user.username + ", \n Here we are informing you about the reminder that you have set regarding " \
                                        "this Note " + note.title
    mail_subject = " Note Reminder for You "
    to_email = email
    send_mail(mail_subject, message, "mdhussainsabhussain@gmail.com", [to_email], fail_silently=False)
    logger.info(" Email Successfully sent for the user %s with mail id %s ", user, to_email)
    note.remainder = None
    note.save()