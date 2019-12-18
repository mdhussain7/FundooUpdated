import requests
from django.contrib.auth.models import User
from urllib3.util import url

from .models import Notes
from celery.task import task
import datetime
from celery import Celery, shared_task
from django.core.mail import send_mail
import logging
from fundoo.settings import fh, BASE_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
app = Celery()

@task
def sent_mail():
    requests.get(url=BASE_URL + 'Celery/')
