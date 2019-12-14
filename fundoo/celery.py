from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.settings')

app = Celery('fundoo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'note.tasks.get_remainders',
        'schedule': 30.0,
    },
}