import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.settings')

app = Celery('fundoo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'notes.tasks.get_remainders',
        # 'schedule': 30.0,
        'schedule':crontab(),
    },
}
