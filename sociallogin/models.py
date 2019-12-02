from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class CreateNotes(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    filename = models.CharField(max_length=30)


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)
