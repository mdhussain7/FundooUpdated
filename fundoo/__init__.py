from __future__ import absolute_import, unicode_literals
from .celeryService import app as celery_app
__all__ = ['celery_app']